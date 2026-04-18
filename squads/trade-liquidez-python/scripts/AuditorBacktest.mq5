//+------------------------------------------------------------------+
//|                                            AuditorBacktest.mq5   |
//|                                     v2.1 PRO Auditor Elite        |
//+------------------------------------------------------------------+
#property copyright "AIOX Squad"
#property version   "2.10"
#property script_show_inputs

void OnStart()
{
   string symbol = Symbol();
   string filename = "audit_backtest_" + symbol + ".csv";
   int handle = FileOpen(filename, FILE_READ|FILE_CSV|FILE_ANSI|FILE_SHARE_READ, ',');
   
   if(handle == INVALID_HANDLE) {
      MessageBox("Arquivo " + filename + " nao encontrado.", "Erro", MB_ICONERROR);
      return;
   }

   ObjectsDeleteAll(0, "AUDIT_");
   int count = 0;
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   double offset = 20 * point;

   // Pula cabecalho (agora com 7 colunas)
   for(int j=0; j<7; j++) FileReadString(handle);

   while(!FileIsEnding(handle))
   {
      string type = FileReadString(handle);
      if(type == "") continue;
      
      double price = StringToDouble(FileReadString(handle));
      datetime t_time = StringToTime(FileReadString(handle));
      double pnl = StringToDouble(FileReadString(handle));
      double z_price = StringToDouble(FileReadString(handle));
      string rsi = FileReadString(handle);
      string trend = FileReadString(handle);

      string name = "AUDIT_" + symbol + "_" + (string)count;
      color sig_color = (pnl > 0) ? clrLime : clrRed;
      
      // 1. Desenha a Zona de Liquidez (Retângulo)
      string zone_name = name + "_Z";
      ObjectCreate(0, zone_name, OBJ_RECTANGLE, 0, t_time - 3600, z_price + 10*point, t_time, z_price - 10*point);
      ObjectSetInteger(0, zone_name, OBJPROP_COLOR, (type == "SIGNAL_SELL") ? clrLightCoral : clrLightGreen);
      ObjectSetInteger(0, zone_name, OBJPROP_FILL, true);
      ObjectSetInteger(0, zone_name, OBJPROP_BACK, true);
      ObjectSetInteger(0, zone_name, OBJPROP_SELECTABLE, false);

      // 2. Desenha a Seta
      if(type == "SIGNAL_SELL")
         ObjectCreate(0, name, OBJ_ARROW_DOWN, 0, t_time, price + offset);
      else
         ObjectCreate(0, name, OBJ_ARROW_UP, 0, t_time, price - offset);

      ObjectSetInteger(0, name, OBJPROP_COLOR, sig_color);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, 3);
      
      // 3. Rótulo de Racional
      string lab_name = name + "_L";
      ObjectCreate(0, lab_name, OBJ_TEXT, 0, t_time, (type == "SIGNAL_SELL") ? price + 3*offset : price - 3*offset);
      string trend_txt = (trend == "1") ? "T:UP" : (trend == "-1") ? "T:DOWN" : "T:NEUT";
      ObjectSetString(0, lab_name, OBJPROP_TEXT, DoubleToString(pnl, 2) + " USD (RSI:" + rsi + " " + trend_txt + ")");
      ObjectSetInteger(0, lab_name, OBJPROP_COLOR, sig_color);
      ObjectSetInteger(0, lab_name, OBJPROP_FONTSIZE, 7);
      ObjectSetDouble(0, lab_name, OBJPROP_ANGLE, 90);

      count++;
   }

   FileClose(handle);
   ChartRedraw(0);
   MessageBox("Auditoria Elite Concluida!\nTrades validados: " + (string)count, "Sucesso");
}
