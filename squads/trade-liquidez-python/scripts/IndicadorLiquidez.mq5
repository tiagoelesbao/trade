//+------------------------------------------------------------------+
//|  IndicadorLiquidez.mq5  --  v6.2.0-ict (alinhado com Sprints 1-5)|
//|  Le liquidez_data_<symbol>.csv escrito pelo bot_liquidez.py      |
//+------------------------------------------------------------------+
//  Mudanças v6.20 (2026-04-29):
//   - Header: VERSION + BOT_STATUS
//   - GATE: estado do gate de horário (news embargo / cutoff) — Sprint 1
//   - SESSION: janela ICT atual (Asia early/Judas/London open/...) — Sprint 1
//   - ICT_BIAS: bias D1 + phase H4/H1 + daily range state — Sprint 2
//   - LIQ_ABOVE/LIQ_BELOW: liquidity levels desenhados como linha tracejada — Sprint 2
//   - POSITION: estado de cada posição aberta (profit_R, candles) — Sprint 4
//   - Painel ampliado em 2 colunas (Status | ICT Context)
//+------------------------------------------------------------------+
#property copyright "AIOX Squad"
#property version   "6.20"
#property indicator_chart_window
#property indicator_plots 0

//--- ================================================================
//--- Inputs
//--- ================================================================
input group "=== ZONAS ==="
input int   InpZonePips       = 10;             // Espessura da zona (pips)
input int   InpMaxZones       = 6;              // Max zonas por lado
input bool  InpShowCenterLine = true;           // Linha central pontilhada
input bool  InpShowLabels     = true;           // Labels de preço nas zonas
input bool  InpHighlightNear  = true;           // Destacar zona próxima ao preço
input int   InpNearPips       = 25;             // Raio "zona próxima" em pips
input int   InpMinBarsWidth   = 60;             // Largura mínima da zona em barras M15

input group "=== LIQUIDITY ICT (Sprint 2) ==="
input bool  InpShowLiquidity  = true;           // Mostrar linhas de liquidez ICT
input color InpLiqAboveColor  = C'255,165,0';   // Liquidez above (laranja)
input color InpLiqBelowColor  = C'0,180,255';   // Liquidez below (azul claro)

input group "=== CORES ZONAS ==="
input color InpResColor       = C'190,60,60';
input color InpSupColor       = C'45,155,80';
input color InpNearResColor   = C'255,40,40';
input color InpNearSupColor   = C'0,220,90';

input group "=== PAINEL ==="
input bool  InpShowPanel      = true;           // Mostrar painel de status

//--- ================================================================
//--- Constantes / estado global
//--- ================================================================
#define PFX "LIQ_"

// BOT STATUS
double  g_pnl_today    = 0.0;
double  g_pnl_total    = 0.0;
string  g_version      = "v?";

// GATE (Sprint 1)
int     g_gate_blocked = 0;
string  g_gate_reason  = "open";

// SESSION (Sprint 1)
string  g_sess_id      = "?";
string  g_sess_label   = "?";
int     g_sess_weight  = 0;

// ICT BIAS (Sprint 2)
string  g_ict_bias     = "neutral";
string  g_ict_h4       = "?";
string  g_ict_h1       = "?";
string  g_ict_state    = "?";
int     g_buy_pts      = 12;
int     g_sell_pts     = 12;

// LIQUIDITY (Sprint 2)
double  g_liq_above_price    = 0.0;
string  g_liq_above_kind     = "";
double  g_liq_above_dist     = 0.0;
double  g_liq_below_price    = 0.0;
string  g_liq_below_kind     = "";
double  g_liq_below_dist     = 0.0;

// POSITIONS (Sprint 4) — até 4 posições por par (sistema permite 1 mas defensivo)
struct PosInfo {
   string  type;
   double  profit_R;
   int     candles;
   double  sl;
   double  tp;
};
PosInfo g_positions[4];
int     g_n_positions = 0;

// EXIT HINT (Sprint 4 ext.) — próxima ação prevista pelo Exit War Room
bool    g_hint_present = false;
string  g_hint_type    = "";
double  g_hint_profit  = 0.0;
int     g_hint_candles = 0;
string  g_hint_action  = "none";   // 'be'|'partial_be'|'close'|'flag'|'none'
string  g_hint_rule    = "-";      // 'a'..'f' ou '-'
string  g_hint_reason  = "";

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
//| Loop principal: le CSV e desenha tudo                            |
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

   //--- Reset estado por ciclo
   g_n_positions = 0;
   g_liq_above_price = 0.0; g_liq_below_price = 0.0;
   g_hint_present = false;

   //--- Le exit_hint_<symbol>.csv se existir (Sprint 4 ext.)
   ReadExitHint(sym);

   //--- Buffers locais para zonas
   double   resPrice[]; datetime resTime[]; int nRes = 0;
   double   supPrice[]; datetime supTime[]; int nSup = 0;
   double   bePrice[];  string   beType[];  int nBe  = 0;

   while(!FileIsEnding(fh))
   {
      string c1 = FileReadString(fh);
      if(c1 == "" || c1 == "HEADER" || c1 == "type") continue;

      // ── VERSION (Sprint 5)
      if(c1 == "VERSION")
      {
         g_version = FileReadString(fh);
         continue;
      }

      // ── BOT_STATUS (legado)
      if(c1 == "BOT_STATUS")
      {
         g_pnl_today = StringToDouble(FileReadString(fh));
         g_pnl_total = StringToDouble(FileReadString(fh));
         FileReadString(fh);   // exaur_zones (legado, descartado)
         continue;
      }

      // ── GATE (Sprint 1)
      if(c1 == "GATE")
      {
         g_gate_blocked = (int)StringToInteger(FileReadString(fh));
         g_gate_reason  = FileReadString(fh);
         continue;
      }

      // ── SESSION (Sprint 1)
      if(c1 == "SESSION")
      {
         g_sess_id     = FileReadString(fh);
         g_sess_label  = FileReadString(fh);
         g_sess_weight = (int)StringToInteger(FileReadString(fh));
         continue;
      }

      // ── ICT_BIAS (Sprint 2)
      if(c1 == "ICT_BIAS")
      {
         g_ict_bias  = FileReadString(fh);
         g_ict_h4    = FileReadString(fh);
         g_ict_h1    = FileReadString(fh);
         g_ict_state = FileReadString(fh);
         g_buy_pts   = (int)StringToInteger(FileReadString(fh));
         g_sell_pts  = (int)StringToInteger(FileReadString(fh));
         continue;
      }

      // ── LIQ_ABOVE / LIQ_BELOW (Sprint 2)
      if(c1 == "LIQ_ABOVE")
      {
         g_liq_above_price = StringToDouble(FileReadString(fh));
         g_liq_above_kind  = FileReadString(fh);
         g_liq_above_dist  = StringToDouble(FileReadString(fh));
         continue;
      }
      if(c1 == "LIQ_BELOW")
      {
         g_liq_below_price = StringToDouble(FileReadString(fh));
         g_liq_below_kind  = FileReadString(fh);
         g_liq_below_dist  = StringToDouble(FileReadString(fh));
         continue;
      }

      // ── POSITION (Sprint 4)
      if(c1 == "POSITION")
      {
         string ttype = FileReadString(fh);
         double pR    = StringToDouble(FileReadString(fh));
         int    cdl   = (int)StringToInteger(FileReadString(fh));
         double sl    = StringToDouble(FileReadString(fh));
         double tp    = StringToDouble(FileReadString(fh));
         if(g_n_positions < 4)
         {
            g_positions[g_n_positions].type     = ttype;
            g_positions[g_n_positions].profit_R = pR;
            g_positions[g_n_positions].candles  = cdl;
            g_positions[g_n_positions].sl       = sl;
            g_positions[g_n_positions].tp       = tp;
            g_n_positions++;
         }
         continue;
      }

      // ── BREAKEVEN (legado)
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

      // ── ZONE_RESISTANCE / ZONE_SUPPORT (legado)
      double   price = StringToDouble(FileReadString(fh));
      datetime t     = StringToTime(FileReadString(fh));
      if(price == 0.0) continue;

      if(c1 == "ZONE_RESISTANCE" && nRes < InpMaxZones)
      {
         ArrayResize(resPrice, nRes + 1);
         ArrayResize(resTime,  nRes + 1);
         resPrice[nRes] = price;
         resTime[nRes]  = t;
         nRes++;
      }
      else if(c1 == "ZONE_SUPPORT" && nSup < InpMaxZones)
      {
         ArrayResize(supPrice, nSup + 1);
         ArrayResize(supTime,  nSup + 1);
         supPrice[nSup] = price;
         supTime[nSup]  = t;
         nSup++;
      }
   }
   FileClose(fh);

   //--- Desenhar zonas
   for(int i = 0; i < nRes; i++)
      DrawZone(i,       resPrice[i], resTime[i], true,  bid, halfZone, nearDist);
   for(int i = 0; i < nSup; i++)
      DrawZone(nRes+i,  supPrice[i], supTime[i], false, bid, halfZone, nearDist);

   //--- Linhas de breakeven (legado)
   for(int i = 0; i < nBe; i++)
      DrawBreakevenLine(i, bePrice[i], beType[i]);

   //--- Liquidity levels ICT (Sprint 2)
   if(InpShowLiquidity)
   {
      if(g_liq_above_price > 0.0)
         DrawLiquidityLine("ABOVE", g_liq_above_price, g_liq_above_kind, true);
      if(g_liq_below_price > 0.0)
         DrawLiquidityLine("BELOW", g_liq_below_price, g_liq_below_kind, false);
   }

   //--- Painel ampliado
   if(InpShowPanel) DrawPanel();

   ChartRedraw(0);
}

//+------------------------------------------------------------------+
//| Le exit_hint_<symbol>.csv escrito pelo Exit War Room             |
//| Formato: HINT,<type>,<profit_R>,<candles>,<action>,<rule>,<reason> |
//+------------------------------------------------------------------+
void ReadExitHint(string sym)
{
   string hintFile = "exit_hint_" + sym + ".csv";
   int fh = FileOpen(hintFile, FILE_READ|FILE_CSV|FILE_ANSI|FILE_SHARE_READ, ',');
   if(fh == INVALID_HANDLE) return;   // sem hint = sem posição monitorada

   while(!FileIsEnding(fh))
   {
      string c1 = FileReadString(fh);
      if(c1 == "" || c1 == "HEADER") continue;
      if(c1 == "HINT")
      {
         g_hint_type    = FileReadString(fh);
         g_hint_profit  = StringToDouble(FileReadString(fh));
         g_hint_candles = (int)StringToInteger(FileReadString(fh));
         g_hint_action  = FileReadString(fh);
         g_hint_rule    = FileReadString(fh);
         g_hint_reason  = FileReadString(fh);
         g_hint_present = true;
         break;
      }
   }
   FileClose(fh);
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
   int   lWidth = isNear ? 2 : 1;

   double hi = price + halfZone;
   double lo = price - halfZone;

   datetime minLeft = (datetime)(TimeCurrent() - (long)InpMinBarsWidth * 15 * 60);
   datetime zLeft   = (t > 0 && t < minLeft) ? t : minLeft;

   string nRect = PFX + "R" + (string)idx;
   string nLine = PFX + "L" + (string)idx;
   string nText = PFX + "T" + (string)idx;

   if(ObjectCreate(0, nRect, OBJ_RECTANGLE, 0, zLeft, hi, TimeCurrent(), lo))
   {
      ObjectSetInteger(0, nRect, OBJPROP_COLOR,      zClr);
      ObjectSetInteger(0, nRect, OBJPROP_FILL,       true);
      ObjectSetInteger(0, nRect, OBJPROP_BACK,       true);
      ObjectSetInteger(0, nRect, OBJPROP_WIDTH,      lWidth);
      ObjectSetInteger(0, nRect, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nRect, OBJPROP_HIDDEN,     true);
   }

   datetime lineRight = (datetime)(TimeCurrent() + 3 * 15 * 60);
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

   color  beColor = C'220,175,0';
   bool   isBuy   = (tradeType == "BUY");

   datetime tLeft  = (datetime)(TimeCurrent() - 30 * 15 * 60);
   datetime tRight = (datetime)(TimeCurrent() +  6 * 15 * 60);

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
//| Linha horizontal de liquidity level ICT (Sprint 2)               |
//+------------------------------------------------------------------+
void DrawLiquidityLine(string side, double price, string kind, bool isAbove)
{
   string nLine = PFX + "LIQ_" + side;
   string nText = PFX + "LIQ_T_" + side;
   color  clr   = isAbove ? InpLiqAboveColor : InpLiqBelowColor;

   datetime tLeft  = (datetime)(TimeCurrent() - 40 * 15 * 60);
   datetime tRight = (datetime)(TimeCurrent() +  8 * 15 * 60);

   if(ObjectCreate(0, nLine, OBJ_TREND, 0, tLeft, price, tRight, price))
   {
      ObjectSetInteger(0, nLine, OBJPROP_COLOR,      clr);
      ObjectSetInteger(0, nLine, OBJPROP_STYLE,      STYLE_DASHDOTDOT);
      ObjectSetInteger(0, nLine, OBJPROP_WIDTH,      2);
      ObjectSetInteger(0, nLine, OBJPROP_BACK,       false);
      ObjectSetInteger(0, nLine, OBJPROP_RAY_RIGHT,  false);
      ObjectSetInteger(0, nLine, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nLine, OBJPROP_HIDDEN,     true);
   }

   string lbl = "LIQ " + side + " " + kind + " (" + DoubleToString(price, _Digits) + ")";
   if(ObjectCreate(0, nText, OBJ_TEXT, 0, (datetime)(TimeCurrent() + 15 * 60), price))
   {
      ObjectSetString( 0, nText, OBJPROP_TEXT,       lbl);
      ObjectSetInteger(0, nText, OBJPROP_COLOR,      clr);
      ObjectSetInteger(0, nText, OBJPROP_FONTSIZE,   8);
      ObjectSetInteger(0, nText, OBJPROP_ANCHOR,     isAbove ? ANCHOR_LEFT_LOWER : ANCHOR_LEFT_UPPER);
      ObjectSetInteger(0, nText, OBJPROP_BACK,       false);
      ObjectSetInteger(0, nText, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, nText, OBJPROP_HIDDEN,     false);
   }
}

//+------------------------------------------------------------------+
//| Painel de status ampliado v6.20 (Sprints 1-5)                    |
//+------------------------------------------------------------------+
void DrawPanel()
{
   int xOff = 8;
   int yOff = 30;
   int w    = 380;     // mais largo p/ caber 2 colunas
   int h    = 250;     // mais alto p/ caber Exit Hint
   int pad  = 8;
   int lineH = 14;

   // Fundo
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

   int x = xOff + pad;
   int x2 = xOff + 180;     // segunda coluna
   int y = yOff + pad;

   // ── Coluna 1: STATUS ──
   AddPanelLabel(PFX+"P_VER", "BOT LIQUIDEZ " + g_version,
                 x, y, 9, C'80,160,250');
   y += lineH + 2;

   // P&L
   string todayStr = "Sessao: $" + (g_pnl_today >= 0 ? "+" : "")
                     + DoubleToString(g_pnl_today, 2);
   AddPanelLabel(PFX+"P_PNL_S", todayStr, x, y, 9,
                 g_pnl_today >= 0 ? C'50,200,100' : C'220,70,70');
   y += lineH;

   string totalStr = "Total : $" + (g_pnl_total >= 0 ? "+" : "")
                     + DoubleToString(g_pnl_total, 2);
   AddPanelLabel(PFX+"P_PNL_T", totalStr, x, y, 9,
                 g_pnl_total >= 0 ? C'50,200,100' : C'220,70,70');
   y += lineH + 4;

   // Gate (Sprint 1)
   string gateLbl = (g_gate_blocked == 1) ? "GATE: BLOCKED" : "GATE: OPEN";
   AddPanelLabel(PFX+"P_GATE", gateLbl, x, y, 9,
                 g_gate_blocked == 1 ? C'220,70,70' : C'80,200,120');
   y += lineH;
   if(g_gate_blocked == 1)
   {
      AddPanelLabel(PFX+"P_GATE_R", "  " + g_gate_reason, x, y, 7, C'190,190,190');
      y += lineH;
   }

   // Sessao (Sprint 1)
   string sessLbl = "Sessao: " + g_sess_label + " (" + IntegerToString(g_sess_weight) + "/15)";
   AddPanelLabel(PFX+"P_SESS", sessLbl, x, y, 8, C'180,180,255');
   y += lineH + 4;

   // Posicoes (Sprint 4)
   if(g_n_positions == 0)
   {
      AddPanelLabel(PFX+"P_POS0", "Sem posicao aberta", x, y, 8, C'130,130,130');
      y += lineH;
   }
   else
   {
      for(int i = 0; i < g_n_positions; i++)
      {
         string sign = (g_positions[i].profit_R >= 0) ? "+" : "";
         color clr = (g_positions[i].profit_R >= 0) ? C'50,200,100' : C'220,70,70';
         string pl = g_positions[i].type + " " + sign +
                     DoubleToString(g_positions[i].profit_R, 2) + "R " +
                     "(" + IntegerToString(g_positions[i].candles) + " candles)";
         AddPanelLabel(PFX+"P_POS"+(string)i, pl, x, y, 9, clr);
         y += lineH;
      }
   }

   // Exit Hint — proxima acao prevista pelo Exit War Room (Sprint 4 ext.)
   if(g_hint_present)
   {
      y += 2;
      // Cor depende da ação
      color  hintClr;
      string hintTitle;
      if(g_hint_action == "close")           { hintClr = C'255,90,90';   hintTitle = "EXIT IMMINENT"; }
      else if(g_hint_action == "partial_be") { hintClr = C'255,200,80';  hintTitle = "PARTIAL+BE"; }
      else if(g_hint_action == "be")         { hintClr = C'180,220,80';  hintTitle = "MOVE TO BE"; }
      else if(g_hint_action == "flag")       { hintClr = C'200,150,80';  hintTitle = "TIME FLAG"; }
      else                                    { hintClr = C'130,130,130'; hintTitle = "AGUARDANDO"; }

      AddPanelLabel(PFX+"P_HINT_T",
                    "Exit WR [rule " + g_hint_rule + "]: " + hintTitle,
                    x, y, 9, hintClr);
      y += lineH;
      // Mostra reason truncada
      string reasonShow = g_hint_reason;
      if(StringLen(reasonShow) > 38) reasonShow = StringSubstr(reasonShow, 0, 38) + "...";
      AddPanelLabel(PFX+"P_HINT_R", "  " + reasonShow, x, y, 7, C'170,170,170');
      y += lineH;
   }

   // ── Coluna 2: ICT CONTEXT (Sprint 2) ──
   int y2 = yOff + pad;
   AddPanelLabel(PFX+"P_ICT_T", "[ICT CONTEXT]", x2, y2, 9, C'255,200,80');
   y2 += lineH + 2;

   string biasArrow = (g_ict_bias == "bullish") ? " UP" :
                      (g_ict_bias == "bearish") ? " DOWN" : " FLAT";
   color biasClr = (g_ict_bias == "bullish") ? C'80,220,120' :
                   (g_ict_bias == "bearish") ? C'240,80,80'  : C'180,180,180';
   AddPanelLabel(PFX+"P_BIAS", "Bias D1: " + g_ict_bias + biasArrow, x2, y2, 9, biasClr);
   y2 += lineH;
   AddPanelLabel(PFX+"P_H4", "H4: " + g_ict_h4, x2, y2, 8, C'200,200,200');
   y2 += lineH;
   AddPanelLabel(PFX+"P_H1", "H1: " + g_ict_h1, x2, y2, 8, C'200,200,200');
   y2 += lineH;
   AddPanelLabel(PFX+"P_DRS", "Daily: " + g_ict_state, x2, y2, 7, C'150,150,200');
   y2 += lineH + 4;

   // Alignment scores
   AddPanelLabel(PFX+"P_AL_T", "Alignment ICT:", x2, y2, 8, C'180,180,180');
   y2 += lineH;
   color buyClr = (g_buy_pts >= 18) ? C'80,220,120' :
                  (g_buy_pts >= 12) ? C'200,200,100' : C'240,80,80';
   color sellClr= (g_sell_pts >= 18) ? C'80,220,120' :
                  (g_sell_pts >= 12) ? C'200,200,100' : C'240,80,80';
   AddPanelLabel(PFX+"P_AL_B", "  BUY : " + IntegerToString(g_buy_pts) + "/25", x2, y2, 9, buyClr);
   y2 += lineH;
   AddPanelLabel(PFX+"P_AL_S", "  SELL: " + IntegerToString(g_sell_pts) + "/25", x2, y2, 9, sellClr);
   y2 += lineH + 4;

   // Liquidity proximity
   if(g_liq_above_price > 0.0)
   {
      string liqA = "LIQ above: " + DoubleToString(g_liq_above_dist, 1) + "p (" + g_liq_above_kind + ")";
      AddPanelLabel(PFX+"P_LIQ_A", liqA, x2, y2, 8, InpLiqAboveColor);
      y2 += lineH;
   }
   if(g_liq_below_price > 0.0)
   {
      string liqB = "LIQ below: " + DoubleToString(g_liq_below_dist, 1) + "p (" + g_liq_below_kind + ")";
      AddPanelLabel(PFX+"P_LIQ_B", liqB, x2, y2, 8, InpLiqBelowColor);
      y2 += lineH;
   }
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
