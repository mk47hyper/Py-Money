$(function() {

    con = document.getElementById('contract');
    con = con.value;

    function rate_calc(sales){
            if(sales >= 500 && sales <= 2000){
                return 0.05
            } else if(sales > 2000 && sales <= 5000){
                return 0.1
            } else if(sales > 5000 && sales <= 10000) {
                return 0.15
            } else if(sales > 10000){
                return 0.2
            } else {
                return 0
            }
        }

    if(con === 'salary'){
        var b = document.getElementById("base_pay");
        var d = document.getElementById("days");
        var p = document.getElementById("pay");


        b.addEventListener("input", salPay);
        d.addEventListener("input", salPay);

        function salPay() {

            var one = b.value || 0;
            var two = d.value || 0;

            p.value = ((one / (52 * 5)) * two).toFixed(2);
        }
    } else if(con === 'hourly'){
        var hr = document.getElementById("hour_rate");
        var hw = document.getElementById("hours_worked");
        var or = document.getElementById("overtime_rate");
        var oh = document.getElementById("overtime_hours");
        var p = document.getElementById("pay");


        hr.addEventListener("input", hPay);
        hw.addEventListener("input", hPay);

        function hPay() {

            var hrate = hr.value || 0;
            var hours = hw.value || 0;
            var over = hrate * 1.5;
            var ohours = oh.value || 0;

            if(hours > 40) {
                ohours = hours - 40;
                oh.value = ohours;
                result = 40 * hrate + over * ohours;
            } else {
                result = hrate * hours;
            }
            or.value = over.toFixed(2);;
            p.value = result.toFixed(2);
        }
    } else if(con === 'commission') {
        var s = document.getElementById("sales");
        var crate = document.getElementById("com_rate");
        var p = document.getElementById("pay");

        s.addEventListener("input", comPay);

        function comPay() {
            var sval = s.value || 0;
            crate.value = rate_calc(sval);

            p.value = (sval * rate_calc(sval)).toFixed(2);

        }
    } else if(con === 'salcom'){
         var b = document.getElementById("base_pay");
         var d = document.getElementById("days");
         var s = document.getElementById("sales");
         var crate = document.getElementById("com_rate");
         var p = document.getElementById("pay");


         b.addEventListener("input", salComPay);
         d.addEventListener("input", salComPay);
         s.addEventListener("input", salComPay);

         function salComPay() {

             var one = b.value || 0;
             var two = d.value || 0;
             var sval = s.value || 0;

             crate.value = rate_calc(sval);
             result = ((one / (52 * 5)) * two) + (sval * rate_calc(sval));

             p.value = result.toFixed(2)
         }
    }

});