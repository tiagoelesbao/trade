//+------------------------------------------------------------------+
//|  IndicadorLiquidez.mq5  —  v6.1.3  War Room Redesign            |
//|  Melhorias: zone merging, labels, painel P&L, destaque próximo  |
//+------------------------------------------------------------------+
#property copyright "AIOX Squad"
#property version   "6.13"
#property indicator_chart_window
#property indicator_plots 0

//--- ================================================================
//--- Inputs
//--- ================================================================
input group "=== ZONAS ==="
input int   InpZonePips       = 10;             // Espessura da zona (pips)
input int   InpMaxZones       = 6;              // Máx zonas por lado (suporte / resistência)
input bool  InpShowCenterLine = true;           // Linha central pontilhada
input bool  InpShowLabels     = true;           // Labels de preço nas zonas
input bool  InpHighlightNear  = true;           // Destacar zona próxima ao preço
input int   InpNearPips       = 25;             // Raio "zona próxima" em pips
input int   InpMinBarsWidth   = 60;             // Largura mínima da zona em barras M15

input group "=== CORES ==="
input color InpResColor       = C'190,60,60';   // Resistência (normal)
input color InpSupColor       = C'45,155,80';   // Suporte (normal)
input color InpNearResColor   = C'255,40,40';   // Resistência (próxima ao preço)
input color InpNearSupColor   = C'0,220,90';    // Suporte (próxima ao preço)

input group "=== PAINEL ==="
input bool  InpShowPanel      = true;           // Mostrar painel de status do bot

//--- ================================================================
//--- Constantes
//--- ================================================================
#define PFX "LIQ_"

//--- Dados do bot (lidos do CSV)
double g_pnl_today   = 0.0;
double g_pnl_total   = 0.0;
int    g_exaur_zones = 0;

//+------------------------------------------------------------------+
int OnInit()
{
   EventSetTimer(5);
   UpdateDrawing();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   ObjectsDeleteAll(0, PFX);
   EventKillTimer();
}

void OnTimer() { UpdateDrawing(); }

void OnChartEvent(const int id, const long &lp, const double &dp, const string &sp)
{
   if(id == CHARTEVENT_CHART_CHANGE) UpdateDrawing();
}

//+------------------------------------------------------------------+
//| Loop principal de leitura e desenho                              |
//+------------------------------------------------------------------+
void UpdateDrawing()
{
   string sym      = Symbol();
   string filename = "liquidez_data_" + sym + ".csv";
   int    fh       = FileOpen(filename, FILE_READ|FILE_CSV|FILE_ANSI|FILE_SHARE_READ, ',');
   if(fh == INVALID_HANDLE) return;

   ObjectsDeleteAll(0, PFX);

   double point    = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double pip      = point * 10.0;
   double halfZone = InpZonePips * pip * 0.5;
   double bid      = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double nearDist = InpNearPips * pip;

   //--- Arrays para zonas
   double   resPrice[]; datetime resTime[]; int nRes = 0;
   double   supPrice[]; datetime supTime[]; int nSup = 0;

   //--- Arrays para posições em breakeven
   double bePrice[]; string beType[]; int nBe = 0;

   while(!FileIsEnding(fh))
   {
      string c1 = FileReadString(fh);
      if(c1 == "" || c1 == "HEADER" || c1 == "type") continue;

      //--- Status do bot
      if(c1 == "BOT_STATUS")
      {
         g_pnl_today   = StringToDouble(FileReadString(fh));
         g_pnl_total   = StringToDouble(FileReadString(fh));
         g_exaur_zones = (int)StringToDouble(FileReadString(fh));
         continue;
      }

      //--- Breakeven: formato especial (price, type_string) — tratar antes do genérico
      if(c1 == "BREAKEVEN")
      {
         double p  = StringToDouble(FileReadString(fh));
         string tp = FileReadString(fh);
         if(p != 0.0 && nBe < 8)
         {
            ArrayResize(bePrice, nBe + 1);
            ArrayResize(beType,  nBe + 1);
            bePrice[nBe] = p;
            beType[nBe]  = tp;
            nBe++;
         }
         continue;
      }

      double   price = StringToDouble(FileReadString(fh));
      datetime t     = StringToTime(FileReadString(fh));
      if(price == 0.0) continue;

      //--- Resistência
      if(c1 == "ZONE_RESISTANCE" && nRes < InpMaxZones)
      {
         ArrayResize(resPrice, nRes + 1);
         ArrayResize(resTime,  nRes + 1);
         resPrice[nRes] = price;
         resTime[nRes]  = t;
         nRes++;
      }
      //--- Suporte
      else if(c1 == "ZONE_SUPPORT" && nSup < InpMaxZones)
      {
         ArrayResize(supPrice, nSup + 1);
         ArrayResize(supTime,  nSup + 1);
         supPrice[nSup] = price;
         supTime[nSup]  = t;
         nSup++;
      }
      //--- Sinal SELL (seta para baixo)
      else if(c1 == "SIGNAL_SELL")
      {
         string sn = PFX + "SELL_" + DoubleToString(price, _Digits);
         if(ObjectCreate(0, sn, OBJ_ARROW_DOWN, 0, t, price + halfZone))
         {
            ObjectSetInteger(0, sn, OBJPROP_COLOR,      clrRed);
            ObjectSetInteger(0, sn, OBJPROP_WIDTH,      4);
            ObjectSetInteger(0, sn, OBJPROP_ARROWCODE,  234);
            ObjectSetInteger(0, sn, OBJPROP_SELECTABLE, false);
            ObjectSetInteger(0, sn, OBJPROP_BACK,       false);
         }
      }
      //--- Sinal BUY (seta para cima)
      else if(c1 == "SIGNAL_BUY")
      {
         string sn = PFX + "BUY_" + DoubleToString(price, _Digits);
         if(ObjectCreate(0, sn, OBJ_ARROW_UP, 0, t, price - halfZone))
         {
            ObjectSetInteger(0, sn, OBJPROP_COLOR,      clrLime);
            ObjectSetInteger(0, sn, OBJPROP_WIDTH,      4);
            ObjectSetInteger(0, sn, OBJPROP_ARROWCODE,  233);
            ObjectSetInteger(0, sn, OBJPROP_SELECTABLE, false);
            ObjectSetInteger(0, sn, OBJPROP_BACK,       false);
         }
      }
   }
   FileClose(fh);

   //--- Desenhar zonas
   for(int i = 0; i < nRes; i++)
      DrawZone(i,       resPrice[i], resTime[i], true,  bid, halfZone, nearDist);
   for(int i = 0; i < nSup; i++)
      DrawZone(nRes+i,  supPrice[i], supTime[i], false, bid, halfZone, nearDist);

   //--- Linhas de breakeven
   for(int i = 0; i < nBe; i++)
      DrawBreakevenLine(i, bePrice[i], beType[i]);

   //--- Painel de status
   if(InpShowPanel) DrawPanel();

   ChartRedraw(0);
}

//+------------------------------------------------------------------+
//| Desenha uma zona (retângulo + linha + label)                     |
//+------------------------------------------------------------------+
void DrawZone(int idx, double price, datetime t,
              bool isRes, double bid, double halfZone, double nearDist)
{
   bool  isNear = InpHighlightNear && (MathAbs(bid - price) <= nearDist);
   color zClr   = isNear ? (isRes ? InpNearResColor : InpNearSupColor)
                         : (isRes ? InpResColor      : InpSupColor);
   color fillClr = isNear ? zClr : (color)(zClr & 0x00FFFFFF | 0xB0000000); // leve transparência quando distante
   int   lWidth = isNear ? 2 : 1;

   double hi = price + halfZone;
   double lo = price - halfZone;

   //--- Largura mínima: zona sempre visível com pelo menos InpMinBarsWidth barras M15
   datetime minLeft = (datetime)(TimeCurrent() - (long)InpMinBarsWidth * 15 * 60);
   datetime zLeft   = (t > 0 && t < minLeft) ? t : minLeft;

   string nRect = PFX + "R" + (string)idx;
   string nLine = PFX + "L" + (string)idx;
   string nText = PFX + "T" + (string)idx;

   //--- Retângulo preenchido
   if(ObjectCreate(0, nRect, OBJ_RECTANGLE, 0, zLeft, hi, TimeCurrent(), lo))
   {
      ObjectSetInteger(0, nRect, OBJPROP_COLOR,      zClr);
      ObjectSetInteger(0, nRect, OBJPROP_FILL,       true);
      ObjectSetInteger(0, nRect, OBJPROP_BACK,       true);
      ObjectSetInteger(0, nRect, OBJPROP_WIDTH,      lWidth);
      ObjectSetInteger(0, nRect, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nRect, OBJPROP_HIDDEN,     true);
   }

   //--- Linha central pontilhada (da borda esquerda até o futuro próximo)
   datetime lineRight = (datetime)(TimeCurrent() + 3 * 15 * 60); // 3 barras à frente
   if(InpShowCenterLine &&
      ObjectCreate(0, nLine, OBJ_TREND, 0, zLeft, price, lineRight, price))
   {
      ObjectSetInteger(0, nLine, OBJPROP_COLOR,      zClr);
      ObjectSetInteger(0, nLine, OBJPROP_STYLE,      STYLE_DOT);
      ObjectSetInteger(0, nLine, OBJPROP_WIDTH,      1);
      ObjectSetInteger(0, nLine, OBJPROP_BACK,       false);
      ObjectSetInteger(0, nLine, OBJPROP_RAY_RIGHT,  false);
      ObjectSetInteger(0, nLine, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nLine, OBJPROP_HIDDEN,     true);
   }

   //--- Label de preço (à direita da zona, na borda atual)
   if(InpShowLabels &&
      ObjectCreate(0, nText, OBJ_TEXT, 0, (datetime)(TimeCurrent() + 15 * 60), price))
   {
      string priceStr = DoubleToString(price, _Digits);
      color  txtClr   = isNear ? clrWhite : C'200,200,200';

      ObjectSetString( 0, nText, OBJPROP_TEXT,      priceStr);
      ObjectSetInteger(0, nText, OBJPROP_COLOR,     txtClr);
      ObjectSetInteger(0, nText, OBJPROP_FONTSIZE,  isNear ? 9 : 8);
      ObjectSetInteger(0, nText, OBJPROP_ANCHOR,    isRes ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
      ObjectSetInteger(0, nText, OBJPROP_BACK,      false);
      ObjectSetInteger(0, nText, OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0, nText, OBJPROP_HIDDEN,    false);
   }
}

//+------------------------------------------------------------------+
//| Linha horizontal dourada quando SL foi movido para breakeven     |
//+------------------------------------------------------------------+
void DrawBreakevenLine(int idx, double price, string tradeType)
{
   string nLine = PFX + "BE_L" + (string)idx;
   string nText = PFX + "BE_T" + (string)idx;

   color  beColor = C'220,175,0';          // Dourado
   bool   isBuy   = (tradeType == "BUY");

   datetime tLeft  = (datetime)(TimeCurrent() - 30 * 15 * 60); // 30 barras atrás
   datetime tRight = (datetime)(TimeCurrent() +  6 * 15 * 60); // 6 barras à frente

   //--- Linha tracejada horizontal no preço de entrada
   if(ObjectCreate(0, nLine, OBJ_TREND, 0, tLeft, price, tRight, price))
   {
      ObjectSetInteger(0, nLine, OBJPROP_COLOR,      beColor);
      ObjectSetInteger(0, nLine, OBJPROP_STYLE,      STYLE_DASH);
      ObjectSetInteger(0, nLine, OBJPROP_WIDTH,      2);
      ObjectSetInteger(0, nLine, OBJPROP_BACK,       false);
      ObjectSetInteger(0, nLine, OBJPROP_RAY_RIGHT,  false);
      ObjectSetInteger(0, nLine, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nLine, OBJPROP_HIDDEN,     true);
   }

   //--- Label "▲ BE ✓" ou "▼ BE ✓" à direita da linha
   if(ObjectCreate(0, nText, OBJ_TEXT, 0, (datetime)(TimeCurrent() + 15 * 60), price))
   {
      string lbl = (isBuy ? "^ BE OK" : "v BE OK");
      ObjectSetString( 0, nText, OBJPROP_TEXT,       lbl);
      ObjectSetInteger(0, nText, OBJPROP_COLOR,      beColor);
      ObjectSetInteger(0, nText, OBJPROP_FONTSIZE,   9);
      ObjectSetInteger(0, nText, OBJPROP_ANCHOR,     isBuy ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
      ObjectSetInteger(0, nText, OBJPROP_BACK,       false);
      ObjectSetInteger(0, nText, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nText, OBJPROP_HIDDEN,     false);
   }
}

//+------------------------------------------------------------------+
//| Painel de status do bot (canto superior esquerdo)                |
//+------------------------------------------------------------------+
void DrawPanel()
{
   int xOff  = 8;
   int yOff  = 30;   // Abaixo do nome do símbolo
   int w     = 170;
   int h     = 78;
   int pad   = 8;
   int lineH = 17;

   //--- Fundo
   string bg = PFX + "PANEL_BG";
   if(ObjectCreate(0, bg, OBJ_RECTANGLE_LABEL, 0, 0, 0))
   {
      ObjectSetInteger(0, bg, OBJPROP_CORNER,     CORNER_LEFT_UPPER);
      ObjectSetInteger(0, bg, OBJPROP_XDISTANCE,  xOff);
      ObjectSetInteger(0, bg, OBJPROP_YDISTANCE,  yOff);
      ObjectSetInteger(0, bg, OBJPROP_XSIZE,      w);
      ObjectSetInteger(0, bg, OBJPROP_YSIZE,      h);
      ObjectSetInteger(0, bg, OBJPROP_BGCOLOR,    C'10,10,10');
      ObjectSetInteger(0, bg, OBJPROP_BORDER_TYPE,BORDER_FLAT);
      ObjectSetInteger(0, bg, OBJPROP_COLOR,      C'50,50,50');
      ObjectSetInteger(0, bg, OBJPROP_BACK,       false);
      ObjectSetInteger(0, bg, OBJPROP_SELECTABLE, false);
   }

   //--- Título
   AddPanelLabel(PFX+"PA", "BOT LIQUIDEZ v6.1.3",
                 xOff+pad, yOff+pad, 8, C'80,120,220');

   //--- P&L Sessão
   string todayStr = "Sessao: $"
                     + (g_pnl_today >= 0 ? "+" : "")
                     + DoubleToString(g_pnl_today, 2);
   AddPanelLabel(PFX+"PB", todayStr,
                 xOff+pad, yOff+pad+lineH, 9,
                 g_pnl_today >= 0 ? C'50,200,100' : C'220,70,70');

   //--- P&L Total
   string totalStr = "Total: $"
                     + (g_pnl_total >= 0 ? "+" : "")
                     + DoubleToString(g_pnl_total, 2);
   AddPanelLabel(PFX+"PC", totalStr,
                 xOff+pad, yOff+pad+lineH*2, 9,
                 g_pnl_total >= 0 ? C'50,200,100' : C'220,70,70');

   //--- Zonas exauridas
   AddPanelLabel(PFX+"PD",
                 "Exauridas: " + (string)g_exaur_zones,
                 xOff+pad, yOff+pad+lineH*3, 8, C'110,110,110');
}

//--- Helper para labels do painel
void AddPanelLabel(string name, string text, int x, int y, int fs, color clr)
{
   if(ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0))
   {
      ObjectSetInteger(0, name, OBJPROP_CORNER,    CORNER_LEFT_UPPER);
      ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
      ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
      ObjectSetString( 0, name, OBJPROP_TEXT,      text);
      ObjectSetInteger(0, name, OBJPROP_FONTSIZE,  fs);
      ObjectSetInteger(0, name, OBJPROP_COLOR,     clr);
      ObjectSetInteger(0, name, OBJPROP_BACK,      false);
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0, name, OBJPROP_HIDDEN,    true);
   }
}

//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double   &open[],
                const double   &high[],
                const double   &low[],
                const double   &close[],
                const long     &tick_volume[],
                const long     &volume[],
                const int      &spread[])
{
   return rates_total;
}
//+------------------------------------------------------------------+
