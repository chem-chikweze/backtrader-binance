
# # # # # # # # # //@version=5

# # # # # # # # # indicator(shorttitle="BB", title="Bollinger Bands", overlay=true, timeframe="", timeframe_gaps=true)
# # # # # # # # # length = input.int(20, minval=1)
# # # # # # # # # src = input(close, title="Source")

# # # # # # # # # mult = input.float(2.0, minval=0.001, maxval=50, title="StdDev")
# # # # # # # # # basis = ta.sma(src, length)
# # # # # # # # # dev = mult * ta.stdev(src, length)

# # # # # # # # # upper = basis + dev
# # # # # # # # # lower = basis - dev
# # # # # # # # # offset = input.int(0, "Offset", minval = -500, maxval = 500)

# # # # # # # # # plot(basis, "Basis", color=#FF6D00, offset = offset)
# # # # # # # # # p1 = plot(upper, "Upper", color=#2962FF, offset = offset)
# # # # # # # # # p2 = plot(lower, "Lower", color=#2962FF, offset = offset)

# # # # # # # # # fill(p1, p2, title = "Background", color=color.rgb(33, 150, 243, 95))


# # # # # # # # //@version=3
# # # # # # # # ////////////////////////////////////////////////////////////
# # # # # # # # //  Copyright by El Jefe/number_juan v0.0.2  -- 1/8/2020
# # # # # # # # // This Indicator is a fixed moving average indicator. By "fixed" I mean
# # # # # # # # // that you can choose for the MA to be based on the current resolution or fixed on 
# # # # # # # # // a specific timeframe. Default will be 128 D MA as inspired by Chart Vampire. 
# # # # # # # # ////////////////////////////////////////////////////////////
# # # # # # # # study("Fixed 128 Day MA", shorttitle="Fixed MA", overlay = true)

# # # # # # # # //inputs
# # # # # # # # inprice = input(close, title="Price Source For The Moving Averages")
# # # # # # # # MA_length = input(128, minval=1, title = "Moving Average Length")
# # # # # # # # useCurrentRes = input(false, title="Use Current Chart Resolution?")
# # # # # # # # // resCustom = input(title="Use Different Timeframe? Uncheck Box Above", type=resolution, defval="D")

# # # # # # # # resCustom = input(title="Use Different Timeframe? Uncheck Box Above", defval="1D", options=["1min", "3min", "5min", "10min","15min", "30min", "45min", "1h", "2h", "3h", "4h", "6h", "8h", "12h", "1D", "2D", "3D", "1W"])
# # # # # # # # resCustomVal = (resCustom == "1min") ? tostring(1) :
# # # # # # # #   (resCustom == "3min") ? tostring(3) :
# # # # # # # #   (resCustom == "5min") ? tostring(5) :
# # # # # # # #   (resCustom == "10min") ? tostring(10) :
# # # # # # # #   (resCustom == "15min") ? tostring(15) :
# # # # # # # #   (resCustom == "30min") ? tostring(30) :
# # # # # # # #   (resCustom == "45min") ? tostring(45) :
# # # # # # # #   (resCustom == "1h") ? tostring(60) :
# # # # # # # #   (resCustom == "2h") ? tostring(120) :
# # # # # # # #   (resCustom == "3h") ? tostring(180) :
# # # # # # # #   (resCustom == "4h") ? tostring(240) :
# # # # # # # #   (resCustom == "6h") ? tostring(360) :
# # # # # # # #   (resCustom == "8h") ? tostring(480) :
# # # # # # # #   (resCustom == "12h") ? tostring(720) :
# # # # # # # #   (resCustom == "1D") ? tostring(1440) :
# # # # # # # #   (resCustom == "2D") ? tostring(2880) :
# # # # # # # #   (resCustom == "3D") ? tostring(4320) :
# # # # # # # #   (resCustom == "1W") ? tostring(10080) :
# # # # # # # #  ""

# # # # # # # # res = useCurrentRes ? period : resCustomVal



# # # # # # # # // MA calculation
# # # # # # # # smoothinput = input(1, minval=1, maxval=4, title='Moving Average Calculation: (1 = SMA), (2 = EMA), (3 = WMA), (4 = Linear)')
# # # # # # # # MA = smoothinput == 1 ? security(tickerid, res, sma(inprice, MA_length)) :
# # # # # # # #  smoothinput == 2 ? security(tickerid, res, ema(inprice, MA_length)) :
# # # # # # # #  smoothinput == 3 ? security(tickerid, res, wma(inprice, MA_length)) :
# # # # # # # #  smoothinput == 4 ? security(tickerid, res, linreg(inprice, MA_length, 0)) :
# # # # # # # #  na

# # # # # # # # // define trend
# # # # # # # # bullish() => inprice >= MA 
# # # # # # # # bearish() => MA < inprice  

# # # # # # # # //change color of MA
# # # # # # # # bullcolor = #0de5c1
# # # # # # # # bearcolor = #781e8c
# # # # # # # # MAcolor =  bullish() ? bullcolor : bearcolor
 
# # # # # # # # plot(MA, title = "Moving Average", linewidth = 2, editable = true, color= MAcolor)




# # # # # # # //
# # # # # # # // @author LazyBear
# # # # # # # //
# # # # # # # // If you use this code in its original/modified form, do drop me a note. 
# # # # # # # //
# # # # # # # study(title="WaveTrend [LazyBear]", shorttitle="WT_LB")
# # # # # # # n1 = input(10, "Channel Length")
# # # # # # # n2 = input(21, "Average Length")
# # # # # # # obLevel1 = input(60, "Over Bought Level 1")
# # # # # # # obLevel2 = input(53, "Over Bought Level 2")
# # # # # # # osLevel1 = input(-60, "Over Sold Level 1")
# # # # # # # osLevel2 = input(-53, "Over Sold Level 2")
 
# # # # # # # ap = hlc3 
# # # # # # # esa = ema(ap, n1)
# # # # # # # d = ema(abs(ap - esa), n1)
# # # # # # # ci = (ap - esa) / (0.015 * d)
# # # # # # # tci = ema(ci, n2)
 
# # # # # # # wt1 = tci
# # # # # # # wt2 = sma(wt1,4)

# # # # # # # plot(0, color=gray)
# # # # # # # plot(obLevel1, color=red)
# # # # # # # plot(osLevel1, color=green)
# # # # # # # plot(obLevel2, color=red, style=3)
# # # # # # # plot(osLevel2, color=green, style=3)

# # # # # # # plot(wt1, color=green)
# # # # # # # plot(wt2, color=red, style=3)
# # # # # # # plot(wt1-wt2, color=blue, style=area, transp=80)


# # # # # # study("VWAP Stdev Bands v2 Mod", overlay=true)
# # # # # # devUp1 = input(1.28, title="Stdev above (1)")
# # # # # # devDn1 = input(1.28, title="Stdev below (1)")

# # # # # # devUp2 = input(2.01, title="Stdev above (2)")
# # # # # # devDn2 = input(2.01, title="Stdev below (2)")

# # # # # # devUp3 = input(2.51, title="Stdev above (3)")
# # # # # # devDn3 = input(2.51, title="Stdev below (3)")

# # # # # # devUp4 = input(3.09, title="Stdev above (4)")
# # # # # # devDn4 = input(3.09, title="Stdev below (4)")

# # # # # # devUp5 = input(4.01, title="Stdev above (5)")
# # # # # # devDn5 = input(4.01, title="Stdev below (5)")

# # # # # # showDv2 = input(true, type=bool, title="Show second group of bands?")
# # # # # # showDv3 = input(true, type=bool, title="Show third group of bands?")
# # # # # # showDv4 = input(false, type=bool, title="Show fourth group of bands?")
# # # # # # showDv5 = input(false, type=bool, title="Show fifth group of bands?")

# # # # # # showPrevVWAP = input(false, type=bool, title="Show previous VWAP close")

# # # # # # start = security(tickerid, "D", time)

# # # # # # newSession = iff(change(start), 1, 0)

# # # # # # vwapsum = iff(newSession, hl2*volume, vwapsum[1]+hl2*volume)
# # # # # # volumesum = iff(newSession, volume, volumesum[1]+volume)
# # # # # # v2sum = iff(newSession, volume*hl2*hl2, v2sum[1]+volume*hl2*hl2)
# # # # # # myvwap = vwapsum/volumesum
# # # # # # dev = sqrt(max(v2sum/volumesum - myvwap*myvwap, 0))

# # # # # # A=plot(myvwap,style=circles, title="VWAP", color=black)
# # # # # # U1=plot(myvwap + devUp1 * dev,style=circles, title="VWAP Upper", color=gray)
# # # # # # D1=plot(myvwap - devDn1 * dev, style=circles, title="VWAP Lower", color=gray)

# # # # # # U2=plot(showDv2 ? myvwap + devUp2 * dev : na, color=red, title="VWAP Upper (2)")
# # # # # # D2=plot(showDv2 ? myvwap - devDn2 * dev : na, color=green, title="VWAP Lower (2)")

# # # # # # U3=plot(showDv3 ? myvwap + devUp3 * dev : na, title="VWAP Upper (3)", color=red)
# # # # # # D3=plot(showDv3 ? myvwap - devDn3 * dev : na, title="VWAP Lower (3)", color=green)

# # # # # # U4=plot(showDv4 ? myvwap + devUp4 * dev : na, title="VWAP Upper (4)", color=red)
# # # # # # D4=plot(showDv4 ? myvwap - devDn4 * dev : na, title="VWAP Lower (4)", color=green)

# # # # # # U5=plot(showDv5 ? myvwap + devUp5 * dev : na, title="VWAP Upper (5)", color=red)
# # # # # # D5=plot(showDv5 ? myvwap - devDn5 * dev : na, title="VWAP Lower (5)", color=green)
# # # # # # prevwap = iff(newSession, myvwap[1], prevwap[1])
# # # # # # plot(showPrevVWAP ? prevwap : na, style=circles, color=close > prevwap ? green : red)


# # # # # # fill(U1, U2, color=red, transp=90, title="Over Bought Fill 1")
# # # # # # fill(D1, D2, color=green, transp=90, title="Over Sold Fill 1")
# # # # # # fill(U2, U3, color=red, transp=90, title="Over Bought Fill 2")
# # # # # # fill(D2, D3, color=green, transp=90, title="Over Sold Fill 2")
# # # # # # fill(U3, U4, color=red, transp=90, title="Over Bought Fill 3")
# # # # # # fill(D3, D4, color=green, transp=90, title="Over Sold Fill 3")
# # # # # # fill(U4, U5, color=red, transp=90, title="Over Bought Fill 4")
# # # # # # fill(D4, D5, color=green, transp=90, title="Over Sold Fill 4")
# # # # # # fill(A, U1, color=gray, transp=90, title="Middle Fill Up")
# # # # # # fill(A, D1, color=gray, transp=90, title="Middle Fill Down")


# # # # # //@version=5
# # # # # indicator(title="Envelope", shorttitle="Env", overlay=true, timeframe="", timeframe_gaps=true)
# # # # # len = input.int(20, title="Length", minval=1)
# # # # # percent = input(10.0)
# # # # # src = input(close, title="Source")
# # # # # exponential = input(false)
# # # # # basis = exponential ? ta.ema(src, len) : ta.sma(src, len)
# # # # # k = percent/100.0
# # # # # upper = basis * (1 + k)
# # # # # lower = basis * (1 - k)
# # # # # plot(basis, "Basis", color=#FF6D00)
# # # # # u = plot(upper, "Upper", color=#2962FF)
# # # # # l = plot(lower, "Lower", color=#2962FF)
# # # # # fill(u, l, color=color.rgb(33, 150, 243, 95), title="Background")


# # # # //@version=4

# # # # // Volatility Stop MTF
# # # # //  v1.1, 2020.01.27

# # # # // This code may be reused freely, without permission.
# # # # // It was written using the following standards:
# # # # //  • PineCoders Coding Conventions for Pine: http://www.pinecoders.com/coding_conventions/
# # # # //  • PineCoders MTF Selection Framework: https://www.tradingview.com/script/90mqACUV-MTF-Selection-Framework-PineCoders-FAQ/

# # # # study("Volatility Stop MTF", "VStop MTF", true, linktoseries = true)

# # # # // ———————————————————— Inputs
# # # # // {
# # # # vCS0 = "Lime/Red",  vCS1 = "Aqua/Pink"
# # # # vST0 = "Line",      vST1 = "Circles",                                           vST2 = "Diamonds",                  vST3 = "Arrows"
# # # # vTF0 = "0. None.",  vTF1 = "1. Discrete Steps (60min, 1D, 3D, 1W, 1M, 12M)",    vTF2 = "2. Multiple Of Current TF", vTF3 = "3. Fixed TF"

# # # # vSrc                = input(close,  "Source")
# # # # vLength             = input(20,     "Length",                       minval  = 2)
# # # # vFactorATR          = input(2.0,    "ATR Factor",                   minval  = 0.25, step = 0.25)
# # # # vColScheme          = input(vCS1,   "Color Scheme",                 options = [vCS0, vCS1])
# # # # vStyle              = input(vST0,   "Style",                        options = [vST0, vST1, vST2, vST3])
# # # # vThickness          = input(2,      "Line Thickness",               options = [0, 1, 2, 3])
# # # # vColorBars          = input(false,  "Color bars on trend state")
# # # # _2                  = input(true,   "═════════ HTF Selection ══════════")
# # # # vHtfType            = input(vTF2,   "Higher Timeframe Selection",   options=[vTF0, vTF1, vTF2, vTF3])
# # # # vHtfType2           = input(3.,     "  2. Multiple of Current TF",  minval = 1)
# # # # vHtfType3           = input("D",    "  3. Fixed TF",                type = input.resolution)
# # # # vHtfStops           = input(true,   "Early Breaches by chart bars")
# # # # vHtfBreachesMrkr    = input(true,   "  Show Early Breaches")
# # # # vHtfBreachedBars    = input(false,  "  Color bars in limbo")
# # # # vHtfBreachedBg      = input(false,  "  Highlight background in limbo")
# # # # vHtfRepaints        = input(false,  "Repainting HTF")
# # # # vHtfShow            = input(false,  "Show HTF Used")
# # # # vOffsetLabels       = input(3,      "Label Offset")

# # # # var vDefaultScheme  = vColScheme == vCS0
# # # # var vShowCircles    = vStyle     == vST1
# # # # var vShowDiamonds   = vStyle     == vST2
# # # # var vShowArrows     = vStyle     == vST3
# # # # var vHtfOn          = vHtfType   != vTF0
# # # # // }


# # # # // ———————————————————— Functions
# # # # // {
# # # # // —————————— Volatility Stop Function
# # # # f_vStop(_src, _atrLength, _atrFactor) =>
# # # #     var _max     = _src
# # # #     var _min     = _src
# # # #     var _trendUp = true
# # # #     var _stop    = 0.0
# # # #     _atrM        = nz(atr(_atrLength) * _atrFactor, tr)
# # # #     _max         := max(_max, _src)
# # # #     _min         := min(_min, _src)
# # # #     _stop        := nz(_trendUp ? max(_stop, _max - _atrM) : min(_stop, _min + _atrM), _src)
# # # #     _trendUp     := _src - _stop >= 0.0
# # # #     if _trendUp != nz(_trendUp[1], true)
# # # #         _max    := _src
# # # #         _min    := _src
# # # #         _stop   := _trendUp ? _max - _atrM : _min + _atrM
# # # #     [_stop, _trendUp]

# # # # // —————————— PineCoders MTF Selection Framework functions
# # # # // ————— Converts current "timeframe.multiplier" plus the TF into minutes of type float.
# # # # f_resInMinutes() => 
# # # #     _resInMinutes = timeframe.multiplier * (
# # # #       timeframe.isseconds   ? 1. / 60.  :
# # # #       timeframe.isminutes   ? 1.        :
# # # #       timeframe.isdaily     ? 1440.     :
# # # #       timeframe.isweekly    ? 10080.    :
# # # #       timeframe.ismonthly   ? 43800.    : na)

# # # # // ————— Returns resolution of _resolution period in minutes.
# # # # f_tfResInMinutes(_resolution) =>
# # # #     // _resolution: resolution of any TF (in "timeframe.period" string format).
# # # #     security(syminfo.tickerid, _resolution, f_resInMinutes())

# # # # // ————— Given current resolution, returns next step of HTF.
# # # # f_resNextStep(_res) =>
# # # #     // _res: current TF in fractional minutes.
# # # #     _res    <= 1        ? "60" :
# # # #       _res  <= 60       ? "1D" :
# # # #       _res  <= 360      ? "3D" :
# # # #       _res  <= 1440     ? "1W" :
# # # #       _res  <= 10080    ? "1M" : "12M"

# # # # // ————— Returns a multiple of current resolution as a string in "timeframe.period" format usable with "security()".
# # # # f_multipleOfRes(_res, _mult) => 
# # # #     // _res:  current resolution in minutes, in the fractional format supplied by f_resInMinutes() companion function.
# # # #     // _mult: Multiple of current TF to be calculated.
# # # #     // Convert current float TF in minutes to target string TF in "timeframe.period" format.
# # # #     _targetResInMin = _res * max(_mult, 1)
# # # #     // Find best string to express the resolution.
# # # #     _targetResInMin     <= 0.083        ? "5S"  :
# # # #       _targetResInMin   <= 0.251        ? "15S" :
# # # #       _targetResInMin   <= 0.501        ? "30S" :
# # # #       _targetResInMin   <= 1440         ? tostring(round(_targetResInMin)) :
# # # #       _targetResInMin   <= 43800        ? tostring(round(min(_targetResInMin / 1440, 365))) + "D" :
# # # #       tostring(round(min(_targetResInMin / 43800, 12))) + "M"

# # # # // ————— Print a label at end of chart.
# # # # f_htfLabel(_txt, _y, _color, _offsetLabels) => 
# # # #     _t = int(time + (f_resInMinutes() * _offsetLabels * 60000))
# # # #     // Create the label on the dataset's first bar.
# # # #     var _lbl = label.new(_t, _y, _txt, xloc.bar_time, yloc.price, #00000000, label.style_none, color.gray, size.large)
# # # #     if barstate.islast
# # # #         // Rather than delete and recreate the label on every realtime bar update,
# # # #         // simply update the label's information; it's more efficient.
# # # #         label.set_xy(_lbl, _t, _y)
# # # #         label.set_text(_lbl, _txt)
# # # #         label.set_textcolor(_lbl, _color)
# # # # // }


# # # # // ———————————————————— Calcs
# # # # // {
# # # # // ————— HTF calcs
# # # # // Get current resolution in float minutes.
# # # # var vResInMinutes = f_resInMinutes()
# # # # // Get HTF from user-defined mode.
# # # # var vHtf = vHtfType == vTF1 ? f_resNextStep(vResInMinutes) : vHtfType == vTF2 ? f_multipleOfRes(vResInMinutes, vHtfType2) : vHtfType3
# # # # // If current res is not lower than HTF, print warning at right of chart.
# # # # if vHtfOn and vResInMinutes >= f_tfResInMinutes(vHtf)
# # # #     f_htfLabel("Chart\nresolution\nmust be < " + vHtf, sma(high + 3 * tr, 10)[1], color.silver, vOffsetLabels)
# # # # else
# # # #     // Show calculated HTF when needed.
# # # #     if vHtfOn and vHtfShow
# # # #         f_htfLabel(vHtf, sma(high + 3 * tr, 10)[1], color.silver, vOffsetLabels)

# # # # // ————— VStop calcs
# # # # [vStopChartTf, vTrendUpChartTf] = f_vStop(vSrc, vLength, vFactorATR)
# # # # vStop           = not vHtfOn ? vStopChartTf    : vHtfRepaints ? security(syminfo.tickerid, vHtf, vStopChartTf)    : security(syminfo.tickerid, vHtf, vStopChartTf[1],    lookahead = barmerge.lookahead_on)
# # # # vTrendUp        = not vHtfOn ? vTrendUpChartTf : vHtfRepaints ? security(syminfo.tickerid, vHtf, vTrendUpChartTf) : security(syminfo.tickerid, vHtf, vTrendUpChartTf[1], lookahead = barmerge.lookahead_on)
# # # # var vInLimbo    = false
# # # # vHtfBreach      = vHtfOn and vHtfStops and not vInLimbo and cross(close, vStop)
# # # # vTrendReversal  = vTrendUp != vTrendUp[1]
# # # # vInLimbo        := (vInLimbo or vHtfBreach) and vTrendUp == vTrendUp[1]
# # # # // }


# # # # // ———————————————————— Plots
# # # # // {
# # # # // ————— Coloring
# # # # var cGreen  = #00FF00ff, var cGreenDark  = #00FF0080
# # # # var cRed    = #FF0000ff, var cRedDark    = #FF0000b0
# # # # var cAqua   = #00C0FFff, var cAquaDark   = #00C0FF80
# # # # var cPink   = #FF0080ff, var cPinkDark   = #FF008080
# # # # var cOrange = #FF8000ff, var cOrangeDark = #FF8000d0
# # # # vColorUp    = vInLimbo ? vDefaultScheme ? cGreenDark : cAquaDark : vDefaultScheme ? cGreen : cAqua
# # # # vColorDown  = vInLimbo ? vDefaultScheme ? cRedDark   : cPinkDark : vDefaultScheme ? cRed   : cPink
# # # # vColor      = vInLimbo ? vDefaultScheme ? vTrendUp ? cGreenDark : cRedDark : vTrendUp ? cAquaDark : cPinkDark : vDefaultScheme ? vTrendUp ? cGreen : cRed : vTrendUp ? cAqua : cPink
# # # # vColorLine  = vTrendReversal or vHtfBreach ? #00000000 : vColor

# # # # // ————— Plotting
# # # # // Diamonds and arrows
# # # # plotshape(vShowDiamonds or vShowCircles ? vStop : na, "Diamonds & Circles", vShowDiamonds ? shape.diamond : shape.circle, location.absolute, vColor)
# # # # plotchar(vShowArrows and vTrendUp       ? vStop : na, "Arrows Up", "⮝", location.absolute, vColorUp)
# # # # plotchar(vShowArrows and not vTrendUp   ? vStop : na, "Arrows Dn", "⮟", location.absolute, vColorDown)

# # # # // Line and beginning circles
# # # # plot(vThickness != 0 ? vStop : na, "V-Stop",            vColorLine, vThickness)
# # # # plot(vTrendReversal  ? vStop : na, "Beg. Circle",       vColor,     max(vThickness, 1) + 2, plot.style_circles)
# # # # plot(vTrendReversal  ? vStop : na, "Beg. Small circle", #000000ff,  max(vThickness, 1),     plot.style_circles)

# # # # // Early breaches
# # # # vEarlyBreachUp = vHtfBreach and not vTrendReversal and vTrendUp
# # # # vEarlyBreachDn = vHtfBreach and not vTrendReversal and not vTrendUp
# # # # plotshape(vHtfBreachesMrkr and vEarlyBreachUp, "HTF Trend Up BReached",   shape.triangledown, location.abovebar, cRed, size = size.tiny)
# # # # plotshape(vHtfBreachesMrkr and vEarlyBreachDn, "HTF Trend Down Breached", shape.triangleup,   location.belowbar, cRed, size = size.tiny)

# # # # // Bars
# # # # vBarUp = close > open
# # # # barcolor(vHtfBreachedBars and vInLimbo ? vBarUp ? cOrange : cOrangeDark : not vColorBars ? na : vTrendUp ? vBarUp ? cGreen : cGreenDark : vBarUp ? cRed : cRedDark)

# # # # // Background
# # # # bgcolor(vHtfBreachedBg and vInLimbo ? color.silver : na, transp = 90)
# # # # // }


# # # # // ————— Alerts
# # # # alertcondition(vTrendReversal,               "1. V-Stop Trend Reversal",        "V-Stop Trend Reversal")
# # # # alertcondition(vTrendUp and not vTrendUp[1], "2. V-Stop Trend Up",              "V-Stop In Up Trend")
# # # # alertcondition(not vTrendUp and vTrendUp[1], "3. V-Stop Trend Down",            "V-Stop In Down Trend")
# # # # alertcondition(vEarlyBreachUp,               "4. V-Stop HTF Trend Up Breach",   "V-Stop HTF Up Trend Breached")
# # # # alertcondition(vEarlyBreachDn,               "5. V-Stop HTF Trend Down Breach", "V-Stop HTF Dn Trend Breached")


# # # //
# # # // @author LazyBear 
# # # // List of all my indicators: 
# # # // https://docs.google.com/document/d/15AGCufJZ8CIUvwFJ9W-IKns88gkWOKBCvByMEvm5MLo/edit?usp=sharing
# # # // 
# # # study("Anchored Momentum [LazyBear]", shorttitle="AMOM_LB")
# # # src=close
# # # l=input(10, title="Momentum Period")
# # # sl=input(8, title="Signal Period")
# # # sm=input(false, title="Smooth Momentum")
# # # smp=input(7, title="Smoothing Period")
# # # sh=input(false, title="Show Histogram")
# # # eb=input(false, title="Enable Barcolors")
# # # p=2*l+1
# # # amom=100*(((sm?ema(src,smp):src)/(sma(src,p)) - 1))
# # # amoms=sma(amom, sl)
# # # hline(0, title="ZeroLine")
# # # hl=sh ? amoms<0 and amom<0 ? max(amoms, amom) : amoms>0 and amom>0 ? min(amoms, amom) : 0 : na
# # # hlc=(amom>amoms)?(amom<0?orange:green):(amom<0?red:orange)
# # # plot(sh?hl:na, style=histogram, color=hlc, linewidth=2)
# # # plot(amom, color=red, linewidth=2, title="Momentum")
# # # plot(amoms, color=green, linewidth=2, title="Signal")
# # # barcolor(eb?hlc:na)


# # //@version=4
# # // 
# # // THANKS :  
# # // I want to thank the following pine coders that inspired me to create this tool with their code or their way of coding or their ideas.
# # //    - dgtrd              with https://fr.tradingview.com/script/kcqc3J2y-HTF-Candles-by-DGT/
# # //    - KivancOzbilgic     with https://fr.tradingview.com/script/f8PIBdha/
# # //    
# # //
# # // LEGEND :
# # //    - RED   RECTANGLE           : Area with VHF decreasing (ranging market)
# # //    - GREEN RECTANGLE           : Area with VHF increasing (trending market)
# # //    - GREEN TRIANGLE            : VHF reached a new bottom on the last 100 period (possible end of ranging market)
# # //    - RED   TRIANGLE            : VHF reached a new top on the last 100 period (possible end of trending market)
# # //    - RED   CIRCLE              : Candle with VHF decreasing (ranging market)
# # //    - GREEN CIRCLE              : Candle with VHF increasing (trending market)
# # //
# # //
# # // RECOMMENDED VALUES :
# # //    - VHF LENGTH == 28 AND VHF SMOOTHING == (1 OR 9 OR 14)
# # //    - VHF LENGTH == 18 AND VHF SMOOTHING == (1 OR 6 OR 9)
# # //


# # study("{Gunzo} Vertical Horizontal Filter (Trading ranges)", shorttitle="{Gunzo} Vertical Horizontal Filter", overlay=true, max_bars_back=500, max_boxes_count=500)

# # // #########################################################################################################
# # // VARIABLES AND CONSTANTS
# # // #########################################################################################################

# # // global input variables
# # vhf_length          = input(18,                 title="VHF length",                         type=input.integer, minval=3, maxval=100)
# # vhf_source          = input(close,              title="VHF source",                         type=input.source)
# # vhf_timeframe       = input('Current',          title="VHF timeframe",                      options=['Current', 'Higher timeframe', '1', '3', '5', '15', '30', '45', '60', '120', '180', '240', '720', 'D', 'W'])

# # smooth_length       = input(6,                  title="VHF smoothing length",               type=input.integer)
               
# # display_range_box   = input(true,               title="Display ranging market rectangles",  type=input.bool)
# # display_trend_box   = input(false,              title="Display trending market rectangles", type=input.bool)
# # min_box_size        = input(5,                  title="Minimum rectangle size",             type=input.integer)
             
# # display_signal_line = input(false,              title="Display signal line",                type=input.bool)
# # display_top_bottoms = input(true,               title="Display VHF tops and bottoms",       type=input.bool)

# # // intermediate variables 
# # final_timeframe = vhf_timeframe == 'Higher timeframe' ?
# #                  (
# #                    timeframe.period == '1'   ? '5'    : 
# #                    timeframe.period == '3'   ? '10'   :
# #                    timeframe.period == '5'   ? '15'   : 
# #                    timeframe.period == '15'  ? '60'   : 
# #                    timeframe.period == '30'  ? '120'  : 
# #                    timeframe.period == '45'  ? '180'  : 
# #                    timeframe.period == '60'  ? '240'  : 
# #                    timeframe.period == '120' ? '720'  : 
# #                    timeframe.period == '180' ? '720'  : 
# #                    timeframe.period == '240' ? 'D'    : 
# #                    timeframe.period == '720' ? 'D'    :
# #                    timeframe.period == 'D'   ? 'W'    :
# #                    timeframe.period == 'W'   ? 'M'    : 
# #                    timeframe.period == '2W'  ? 'M'    : 
# #                    timeframe.period == 'M'   ? '3M'   : 
# #                    timeframe.period == '3M'  ? '6M'   :
# #                    timeframe.period == '6M'  ? '6M'   :
# #                    '6M'
# #                  ) : ( vhf_timeframe == 'Current' ? timeframe.period : vhf_timeframe)
 
 
# # // #########################################################################################################
# # // VHF CALCULATION
# # // #########################################################################################################

# # // convert resolution as a string to number of minutes
# # fn_convert_resolution_to_minutes(resolution) =>
# #     coeff   = 1 
# #     minutes = resolution == "1" ? 1*coeff : resolution == "2" ? 2*coeff : resolution == "3" ? 3*coeff : resolution == "5" ? 5*coeff : resolution == "15" ? 15*coeff : resolution == "30" ? 30*coeff : resolution == "45" ? 45*coeff : resolution == "60" ? 60*coeff : resolution == "120" ? 120*coeff : resolution == "180" ? 180*coeff : resolution == "240" ? 240*coeff : resolution == "720" ? 720*coeff : resolution == "D" ? 1440 : resolution == "W" ? 7*1440 : int(na)
# #     minutes

# # // calculate the ratio between current resolution and user input resolution
# # fn_get_timeperiod_multiplier(timeperiod_src) =>
# #     minutes_src    = fn_convert_resolution_to_minutes(timeperiod_src)
# #     minutes_dest   = floor( (time - time[1]) / (60 * 1000.0) )
# #     multiplier     = minutes_src > minutes_dest ? int(minutes_src / minutes_dest) : 1
# #     multiplier
    
# # // vhf calculation
# # fn_calculate_vhf(vhf_source, vhf_length) =>
# #     hcp = highest(vhf_source, vhf_length)
# #     lcp = lowest(vhf_source,  vhf_length)
# #     mcp = sum(abs(change(vhf_source)), vhf_length)
# #     vhf = (hcp - lcp) / mcp
# #     vhf
# # // recuperate raw data from higher
# # vhf_htf_raw = security(syminfo.tickerid, final_timeframe, fn_calculate_vhf(vhf_source, vhf_length))

# # // get the multiplier between current time frame and time frame selected in the input
# # timeperiod_multiplier = fn_get_timeperiod_multiplier(final_timeframe)

# # // interpolate the data by smoothening between missing data
# # vhf = sma(vhf_htf_raw,  timeperiod_multiplier)

# # // vhf smoothed calculation
# # vhf_smooth       = ema(vhf, smooth_length)

# # // derivated calculations
# # vhf_trend_up     = vhf_smooth > vhf_smooth[1]
# # vhf_trend_down   = not vhf_trend_up
# # vhf_smooth_color = vhf_smooth > vhf_smooth[1] ? color.green : color.red

# # // top/bottoms calculations
# # vhf_high_100     = highest(vhf_smooth, 100)
# # vhf_low_100      = lowest(vhf_smooth, 100)
# # vhf_new_top      = vhf_smooth > vhf_high_100[1] 
# # vhf_new_bottom   = vhf_smooth < vhf_low_100[1]


# # // #########################################################################################################
# # // RANGE BOX CALCULATIONS
# # // #########################################################################################################

# # // ranging market rectangle variables
# # range_box_begin_time    = int(na)
# # range_box_begin_time   := vhf_trend_up[1] and vhf_trend_down ? bar_index[1] : vhf_trend_down[1] and vhf_trend_down ? range_box_begin_time[1] : na
# # range_box_end_time      = bar_index
# # range_box_drawing       = not na(range_box_begin_time)
# # range_box_length        = range_box_drawing ? range_box_end_time - range_box_begin_time : 1
# # range_box_begin_price   = highest(high, range_box_length)
# # range_box_end_price     = lowest(low,   range_box_length) 
# # range_box_overwrite     = not na(range_box_begin_time) and not na(range_box_begin_time[1])
# # range_box_end_drawing   = na(range_box_begin_time) and not na(range_box_begin_time[1])
# # range_box_too_small     = range_box_end_drawing and range_box_length[1] < min_box_size

# # // trending market rectangle variables
# # trend_box_begin_time    = int(na)
# # trend_box_begin_time   := vhf_trend_down[1] and vhf_trend_up ? bar_index[1] : vhf_trend_up[1] and vhf_trend_up ? trend_box_begin_time[1] : na
# # trend_box_end_time      = bar_index
# # trend_box_drawing       = not na(trend_box_begin_time)
# # trend_box_length        = trend_box_drawing ? trend_box_end_time - trend_box_begin_time : 1
# # trend_box_begin_price   = highest(high, trend_box_length)
# # trend_box_end_price     = lowest(low,   trend_box_length) 
# # trend_box_overwrite     = not na(trend_box_begin_time) and not na(trend_box_begin_time[1])
# # trend_box_end_drawing   = na(trend_box_begin_time) and not na(trend_box_begin_time[1])
# # trend_box_too_small     = trend_box_end_drawing and trend_box_length[1] < min_box_size


# # // #########################################################################################################
# # // PLOTTING ON CHART
# # // #########################################################################################################

# # // display ranging market rectangle
# # var box range_box = na
# # if display_range_box
# #     if range_box_overwrite or range_box_too_small
# #         box.delete(range_box) 
# #     if range_box_drawing
# #         range_box := box.new(range_box_begin_time, range_box_begin_price, range_box_end_time, range_box_end_price, color.red, 1, line.style_dotted, extend.none, xloc.bar_index, color.new(color.red, 85))
        
# # // display trending market rectangle        
# # var box trend_box = na
# # if display_trend_box
# #     if trend_box_overwrite or trend_box_too_small
# #         box.delete(trend_box) 
# #     if trend_box_drawing
# #         trend_box := box.new(trend_box_begin_time, trend_box_begin_price, trend_box_end_time, trend_box_end_price, color.green, 1, line.style_dotted, extend.none, xloc.bar_index, color.new(color.green, 85))


# # // #########################################################################################################
# # // PLOTTING SIGNALS
# # // #########################################################################################################

# # plotshape(display_signal_line and vhf_trend_down, title='Trend down', style=shape.circle,       location=location.bottom,   size=size.small, color=color.new(color.red,50))
# # plotshape(display_signal_line and vhf_trend_up,   title='Trend up',   style=shape.circle,       location=location.bottom,   size=size.small, color=color.new(color.green,50))

# # plotshape(display_top_bottoms and vhf_new_top,    title='New top',    style=shape.triangledown, location=location.abovebar, size=size.small, color=color.red)
# # plotshape(display_top_bottoms and vhf_new_bottom, title='New bottom', style=shape.triangleup,   location=location.belowbar, size=size.small, color=color.green)


# # // #########################################################################################################
# # // PLOTTING DEBUG VARIABLES
# # // #########################################################################################################

# # //plot(fn_convert_resolution_to_minutes(final_timeframe), "minutes_src")
# # //plot(floor( (time - time[1]) / (60 * 1000.0)), "minutes_dest")
# # //plot(timeperiod_multiplier, "timeperiod_multiplier")
# # //plot(vhf_smooth, linewidth=3, color=vhf_smooth_color)
# # //plot(vhf_high_100, linewidth=3, color=color.green)
# # //plot(vhf_low_100, linewidth=3, color=color.red)
# # //plot(vhf, linewidth=3, color=color.white)
# # //plot(vhf_htf_raw, color=color.yellow) 




# study(title="JKSW Strength momentum index v2", shorttitle="JKSW SMI v2")

# // Plot the RSI 
# src = input(ohlc4, "Source")

# shortlen = input(10, "Short term bars", integer)
# midlen = input(35, "Mid term bars", integer)
# longlen = input(110, "Long term bars", integer)

# shortup = rma(max(change(src), 0), shortlen)
# shortdown = rma(-min(change(src), 0), shortlen)

# midup = rma(max(change(src), 0), midlen)
# middown = rma(-min(change(src), 0), midlen)

# longup = rma(max(change(src), 0), longlen)
# longdown = rma(-min(change(src), 0), longlen)

# short = shortdown == 0 ? 100 : shortup == 0VDUB_BINARY_PRO_3_V2 ? 0 : 100 - (100 / (1 + shortup / shortdown))
# mid = middown == 0 ? 100 : midup == 0 ? 0 : 100 - (100 / (1 + midup / middown))
# long = longdown == 0 ? 100 : longup == 0 ? 0 : 100 - (100 / (1 + longup / longdown))

# // Overbought line
# hline(80, "Overbought", black, dotted, 2)
# // Oversold line
# hline(20, "Oversold", black, dotted, 2)
# // Mid line
# hline(50, "Mid line", black, dotted)

# // Plot on the chart where the points cross
# color = short > mid ? short > long ? green : yellow : short < long ? red : yellow 
# plot(short, color=color, title="SMI")
# barcolor(color)
