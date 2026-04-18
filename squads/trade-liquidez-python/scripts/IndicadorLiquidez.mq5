//+------------------------------------------------------------------+
//|                                            IndicadorLiquidez.mq5 |
//|                                     v5.5 Multi-Pair Sniper Edition |
//+------------------------------------------------------------------+
#property copyright "AIOX Squad"
#property link      ""
#property version   "5.50"
#property indicator_chart_window

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
   EventSetTimer(5); // Sincronia a cada 5 segundos
   UpdateDrawing();
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                       |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   ObjectsDeleteAll(0, "LIQ_");
   EventKillTimer();
}

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
{
   UpdateDrawing();
}

//+------------------------------------------------------------------+
//| Função principal de leitura e desenho                            |
//+------------------------------------------------------------------+
void UpdateDrawing()
{
   // DETECÇÃO AUTOMÁTICA DO ARQUIVO POR ATIVO
   string symbol = Symbol();
   string filename = "liquidez_data_" + symbol + ".csv";

   // Abre o arquivo específico do ativo
   int handle = FileOpen(filename, FILE_READ|FILE_CSV|FILE_ANSI|FILE_SHARE_READ, ',');
   if(handle == INVALID_HANDLE) return;

   // Limpa desenhos antigos do ativo para atualizar
   ObjectsDeleteAll(0, "LIQ_");

   int i = 0;
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   while(!FileIsEnding(handle))
   {
      string type = FileReadString(handle);
      
      // Pula cabeçalhos ou linhas vazias
      if(type == "" || type == "HEADER" || type == "type") continue;
      
      string price_str = FileReadString(handle);
      if(price_str == "") continue;
      
      double price = StringToDouble(price_str);
      string time_str = FileReadString(handle);
      if(time_str == "") continue;
      
      datetime t_start = StringToTime(time_str);

      string name = "LIQ_" + symbol + "_" + (string)i;
      
      if(type == "ZONE_RESISTANCE")
      {
         ObjectCreate(0, name, OBJ_RECTANGLE, 0, t_start, price + 10*point, TimeCurrent(), price - 10*point);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLightCoral);
         ObjectSetInteger(0, name, OBJPROP_FILL, true);
         ObjectSetInteger(0, name, OBJPROP_BACK, true);
         ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      }
      else if(type == "ZONE_SUPPORT")
      {
         ObjectCreate(0, name, OBJ_RECTANGLE, 0, t_start, price + 10*point, TimeCurrent(), price - 10*point);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLightGreen);
         ObjectSetInteger(0, name, OBJPROP_FILL, true);
         ObjectSetInteger(0, name, OBJPROP_BACK, true);
         ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      }
      else if(type == "SIGNAL_SELL")
      {
         ObjectCreate(0, name, OBJ_ARROW_DOWN, 0, TimeCurrent(), price);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed);
         ObjectSetInteger(0, name, OBJPROP_WIDTH, 4);
      }
      else if(type == "SIGNAL_BUY")
      {
         ObjectCreate(0, name, OBJ_ARROW_UP, 0, TimeCurrent(), price);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLime);
         ObjectSetInteger(0, name, OBJPROP_WIDTH, 4);
      }
      
      i++;
   }

   FileClose(handle);
   ChartRedraw(0);
}

//+------------------------------------------------------------------+
//| Standard OnCalculate                                             |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   return(rates_total);
}
