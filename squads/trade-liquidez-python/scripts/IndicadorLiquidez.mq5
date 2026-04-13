//+------------------------------------------------------------------+
//|                                            IndicadorLiquidez.mq5 |
//+------------------------------------------------------------------+
#property copyright "AIOX Squad"
#property link      ""
#property version   "1.00"
#property indicator_chart_window

//--- input parameters
input string   Filename = "liquidez_data.csv";

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
   EventSetTimer(5); // Atualiza a cada 5 segundos
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
//| Custom indicator iteration function                              |
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
   UpdateDrawing();
   return(rates_total);
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
   // Adicionado FILE_SHARE_READ para permitir leitura enquanto o Python escreve
   int handle = FileOpen(Filename, FILE_READ|FILE_CSV|FILE_ANSI|FILE_SHARE_READ, ',');
   if(handle == INVALID_HANDLE) return;

   // Limpa desenhos antigos para atualizar
   ObjectsDeleteAll(0, "LIQ_");

   int i = 0;
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);

   while(!FileIsEnding(handle))
   {
      string type = FileReadString(handle);
      
      // Pula qualquer tipo de cabeçalho ou linha vazia
      if(type == "" || type == "HEADER" || type == "type" || type == "DATA") continue;
      
      string price_str = FileReadString(handle);
      if(price_str == "" || price_str == "price") continue;
      
      double price = StringToDouble(price_str);
      string time_str = FileReadString(handle);
      if(time_str == "" || time_str == "time") continue;
      
      datetime t_start = StringToTime(time_str);

      string name = "LIQ_" + (string)i;
      
      if(type == "ZONE_RESISTANCE")
      {
         ObjectCreate(0, name, OBJ_RECTANGLE, 0, t_start, price + 5*point, TimeCurrent(), price - 5*point);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLightCoral);
         ObjectSetInteger(0, name, OBJPROP_FILL, true);
         ObjectSetInteger(0, name, OBJPROP_BACK, true);
      }
      else if(type == "ZONE_SUPPORT")
      {
         ObjectCreate(0, name, OBJ_RECTANGLE, 0, t_start, price + 5*point, TimeCurrent(), price - 5*point);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLightGreen);
         ObjectSetInteger(0, name, OBJPROP_FILL, true);
         ObjectSetInteger(0, name, OBJPROP_BACK, true);
      }
      else if(type == "SIGNAL_SELL")
      {
         ObjectCreate(0, name, OBJ_ARROW, 0, TimeCurrent(), price);
         ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 234);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed);
         ObjectSetInteger(0, name, OBJPROP_WIDTH, 3);
      }
      else if(type == "SIGNAL_BUY")
      {
         ObjectCreate(0, name, OBJ_ARROW, 0, TimeCurrent(), price);
         ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 233);
         ObjectSetInteger(0, name, OBJPROP_COLOR, clrLime);
         ObjectSetInteger(0, name, OBJPROP_WIDTH, 3);
      }
      
      i++;
   }

   FileClose(handle);
   ChartRedraw(0);
}
