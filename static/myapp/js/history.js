let symbol = " €";
let data;

let monday_fc = document.getElementById('monday_fc');
let monday_sc = document.getElementById('monday_sc');
let monday_des = document.getElementById('monday_des');
let monday_dr = document.getElementById('monday_dr');

let monday_fcp = document.getElementById('monday_fcp');
let monday_scp = document.getElementById('monday_scp');
let monday_des_p = document.getElementById('monday_des_p');
let monday_dr_p = document.getElementById('monday_dr_p');

let monday_fcq = document.getElementById('monday_fcq');
let monday_scq = document.getElementById('monday_scq');
let monday_des_q = document.getElementById('monday_des_q');
let monday_dr_q = document.getElementById('monday_dr_q');


let tuesday_fc = document.getElementById('tuesday_fc');
let tuesday_sc = document.getElementById('tuesday_sc');
let tuesday_des = document.getElementById('tuesday_des');
let tuesday_dr = document.getElementById('tuesday_dr');

let tuesday_fcp = document.getElementById('tuesday_fcp');
let tuesday_scp = document.getElementById('tuesday_scp');
let tuesday_des_p = document.getElementById('tuesday_des_p');
let tuesday_dr_p = document.getElementById('tuesday_dr_p');

let tuesday_fcq = document.getElementById('tuesday_fcq');
let tuesday_scq = document.getElementById('tuesday_scq');
let tuesday_des_q = document.getElementById('tuesday_des_q');
let tuesday_dr_q = document.getElementById('tuesday_dr_q');


let wednesday_fc = document.getElementById('wednesday_fc');
let wednesday_sc = document.getElementById('wednesday_sc');
let wednesday_des = document.getElementById('wednesday_des');
let wednesday_dr = document.getElementById('wednesday_dr');

let wednesday_fcp = document.getElementById('wednesday_fcp');
let wednesday_scp = document.getElementById('wednesday_scp');
let wednesday_des_p = document.getElementById('wednesday_des_p');
let wednesday_dr_p = document.getElementById('wednesday_dr_p');

let wednesday_fcq = document.getElementById('wednesday_fcq');
let wednesday_scq = document.getElementById('wednesday_scq');
let wednesday_des_q = document.getElementById('wednesday_des_q');
let wednesday_dr_q = document.getElementById('wednesday_dr_q');


let thursday_fc = document.getElementById('thursday_fc');
let thursday_sc = document.getElementById('thursday_sc');
let thursday_des = document.getElementById('thursday_des');
let thursday_dr = document.getElementById('thursday_dr');

let thursday_fcp = document.getElementById('thursday_fcp');
let thursday_scp = document.getElementById('thursday_scp');
let thursday_des_p = document.getElementById('thursday_des_p');
let thursday_dr_p = document.getElementById('thursday_dr_p');

let thursday_fcq = document.getElementById('thursday_fcq');
let thursday_scq = document.getElementById('thursday_scq');
let thursday_des_q = document.getElementById('thursday_des_q');
let thursday_dr_q = document.getElementById('thursday_dr_q');


let friday_fc = document.getElementById('friday_fc');
let friday_sc = document.getElementById('friday_sc');
let friday_des = document.getElementById('friday_des');
let friday_dr = document.getElementById('friday_dr');

let friday_fcp = document.getElementById('friday_fcp');
let friday_scp = document.getElementById('friday_scp');
let friday_des_p = document.getElementById('friday_des_p');
let friday_dr_p = document.getElementById('friday_dr_p');

let friday_fcq = document.getElementById('friday_fcq');
let friday_scq = document.getElementById('friday_scq');
let friday_des_q = document.getElementById('friday_des_q');
let friday_dr_q = document.getElementById('friday_dr_q');


let monday_total = document.getElementById('monday_total');
let tuesday_total = document.getElementById('tuesday_total');
let wednesday_total = document.getElementById('wednesday_total');
let thursday_total = document.getElementById('thursday_total');
let friday_total = document.getElementById('friday_total');

let total = document.getElementById('total');

$(document).ready(function(){
    
    let fc_prices;
    let sc_prices;
    let des_prices;
    let dr_prices;

    $.ajax({
        type: 'GET',
        url: '/history-set-price/',
        success: function(response){
            data = response['data'];
            fc_prices = data['first_course_prices'];
            sc_prices = data['second_course_prices'];
            des_prices = data['dessert_prices'];
            dr_prices = data['drinks_prices'];

            monday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(monday_fc.innerHTML)] + symbol;
            monday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(monday_sc.innerHTML)] + symbol;
            monday_des_p.innerHTML = des_prices[data['desserts'].indexOf(monday_des.innerHTML)] + symbol;
            monday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(monday_dr.innerHTML)] + symbol;

            tuesday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(tuesday_fc.innerHTML)] + symbol;
            tuesday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(tuesday_sc.innerHTML)] + symbol;
            tuesday_des_p.innerHTML = des_prices[data['desserts'].indexOf(tuesday_des.innerHTML)] + symbol;
            tuesday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(tuesday_dr.innerHTML)] + symbol;

            wednesday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(wednesday_fc.innerHTML)] + symbol;
            wednesday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(wednesday_sc.innerHTML)] + symbol;
            wednesday_des_p.innerHTML = des_prices[data['desserts'].indexOf(wednesday_des.innerHTML)] + symbol;
            wednesday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(wednesday_dr.innerHTML)] + symbol;

            thursday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(thursday_fc.innerHTML)] + symbol;
            thursday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(thursday_sc.innerHTML)] + symbol;
            thursday_des_p.innerHTML = des_prices[data['desserts'].indexOf(thursday_des.innerHTML)] + symbol;
            thursday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(thursday_dr.innerHTML)] + symbol;

            friday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(friday_fc.innerHTML)] + symbol;
            friday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(friday_sc.innerHTML)] + symbol;
            friday_des_p.innerHTML = des_prices[data['desserts'].indexOf(friday_des.innerHTML)] + symbol;
            friday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(friday_dr.innerHTML)] + symbol;

            let m_total = fc_prices[data['first_courses'].indexOf(monday_fc.innerHTML)] * parseInt(monday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(monday_sc.innerHTML)] * parseInt(monday_scq.innerHTML) + des_prices[data['desserts'].indexOf(monday_des.innerHTML)] * parseInt(monday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(monday_dr.innerHTML)] * monday_dr_q.innerHTML;
            let tu_total = fc_prices[data['first_courses'].indexOf(tuesday_fc.innerHTML)] * parseInt(tuesday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(tuesday_sc.innerHTML)] * parseInt(tuesday_scq.innerHTML) + des_prices[data['desserts'].indexOf(tuesday_des.innerHTML)] * parseInt(tuesday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(tuesday_dr.innerHTML)] * tuesday_dr_q.innerHTML;
            let we_total = fc_prices[data['first_courses'].indexOf(wednesday_fc.innerHTML)] * parseInt(wednesday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(wednesday_sc.innerHTML)] * parseInt(wednesday_scq.innerHTML) + des_prices[data['desserts'].indexOf(wednesday_des.innerHTML)] * parseInt(wednesday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(wednesday_dr.innerHTML)] * wednesday_dr_q.innerHTML;
            let th_total = fc_prices[data['first_courses'].indexOf(thursday_fc.innerHTML)] * parseInt(thursday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(thursday_sc.innerHTML)] * parseInt(thursday_scq.innerHTML) + des_prices[data['desserts'].indexOf(thursday_des.innerHTML)] * parseInt(thursday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(thursday_dr.innerHTML)] * thursday_dr_q.innerHTML;
            let fr_total = fc_prices[data['first_courses'].indexOf(friday_fc.innerHTML)] * parseInt(friday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(friday_sc.innerHTML)] * parseInt(friday_scq.innerHTML) + des_prices[data['desserts'].indexOf(friday_des.innerHTML)] * parseInt(friday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(friday_dr.innerHTML)] * friday_dr_q.innerHTML;

            monday_total.innerHTML = m_total + symbol;
            tuesday_total.innerHTML = tu_total + symbol;
            wednesday_total.innerHTML = we_total + symbol;
            thursday_total.innerHTML = th_total + symbol;
            friday_total.innerHTML = fr_total + symbol;

            total.innerHTML = total.innerHTML + (m_total + tu_total + we_total + th_total + fr_total) + symbol;
        }

    });
    
});


$("#date").change(function(){

    $.ajax({
        type:'GET',
        url: '/history-another-week/',
        data: {
            "date": $("#date").val()
        },
        success: function(response){
            if (response["date_exists"] === false) {
                alert("Current date is not valid! Enter the correct one!");
            } else {
                db_data = response['data'];
                data = response['menu'];

                fc_prices = data['first_course_prices'];
                sc_prices = data['second_course_prices'];
                des_prices = data['dessert_prices'];
                dr_prices = data['drinks_prices'];

                monday_fc.innerHTML = db_data['monday']['first_course'];
                monday_sc.innerHTML = db_data['monday']['second_course'];
                monday_des.innerHTML = db_data['monday']['dessert'];
                monday_dr.innerHTML = db_data['monday']['drink'];

                monday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(monday_fc.innerHTML)] + symbol;
                monday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(monday_sc.innerHTML)] + symbol;
                monday_des_p.innerHTML = des_prices[data['desserts'].indexOf(monday_des.innerHTML)] + symbol;
                monday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(monday_dr.innerHTML)] + symbol;

                monday_fcq.innerHTML = db_data['monday']['first_course_quantity'];
                monday_scq.innerHTML = db_data['monday']['second_course_quantity'];
                monday_des_q.innerHTML = db_data['monday']['dessert_quantity'];
                monday_dr_q.innerHTML = db_data['monday']['drink_quantity'];


                tuesday_fc.innerHTML = db_data['tuesday']['first_course'];
                tuesday_sc.innerHTML = db_data['tuesday']['second_course'];
                tuesday_des.innerHTML = db_data['tuesday']['dessert'];
                tuesday_dr.innerHTML = db_data['tuesday']['drink'];

                tuesday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(tuesday_fc.innerHTML)] + symbol;
                tuesday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(tuesday_sc.innerHTML)] + symbol;
                tuesday_des_p.innerHTML = des_prices[data['desserts'].indexOf(tuesday_des.innerHTML)] + symbol;
                tuesday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(tuesday_dr.innerHTML)] + symbol;

                tuesday_fcq.innerHTML = db_data['tuesday']['first_course_quantity'];
                tuesday_scq.innerHTML = db_data['tuesday']['second_course_quantity'];
                tuesday_des_q.innerHTML = db_data['tuesday']['dessert_quantity'];
                tuesday_dr_q.innerHTML = db_data['tuesday']['drink_quantity'];


                wednesday_fc.innerHTML = db_data['wednesday']['first_course'];
                wednesday_sc.innerHTML = db_data['wednesday']['second_course'];
                wednesday_des.innerHTML = db_data['wednesday']['dessert'];
                wednesday_dr.innerHTML = db_data['wednesday']['drink'];

                wednesday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(wednesday_fc.innerHTML)] + symbol;
                wednesday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(wednesday_sc.innerHTML)] + symbol;
                wednesday_des_p.innerHTML = des_prices[data['desserts'].indexOf(wednesday_des.innerHTML)] + symbol;
                wednesday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(wednesday_dr.innerHTML)] + symbol;

                wednesday_fcq.innerHTML = db_data['wednesday']['first_course_quantity'];
                wednesday_scq.innerHTML = db_data['wednesday']['second_course_quantity'];
                wednesday_des_q.innerHTML = db_data['wednesday']['dessert_quantity'];
                wednesday_dr_q.innerHTML = db_data['wednesday']['drink_quantity'];


                thursday_fc.innerHTML = db_data['thursday']['first_course'];
                thursday_sc.innerHTML = db_data['thursday']['second_course'];
                thursday_des.innerHTML = db_data['thursday']['dessert'];
                thursday_dr.innerHTML = db_data['thursday']['drink'];

                thursday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(thursday_fc.innerHTML)] + symbol;
                thursday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(thursday_sc.innerHTML)] + symbol;
                thursday_des_p.innerHTML = des_prices[data['desserts'].indexOf(thursday_des.innerHTML)] + symbol;
                thursday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(thursday_dr.innerHTML)] + symbol;

                thursday_fcq.innerHTML = db_data['thursday']['first_course_quantity'];
                thursday_scq.innerHTML = db_data['thursday']['second_course_quantity'];
                thursday_des_q.innerHTML = db_data['thursday']['dessert_quantity'];
                thursday_dr_q.innerHTML = db_data['thursday']['drink_quantity'];


                friday_fc.innerHTML = db_data['friday']['first_course'];
                friday_sc.innerHTML = db_data['friday']['second_course'];
                friday_des.innerHTML = db_data['friday']['dessert'];
                friday_dr.innerHTML = db_data['friday']['drink'];

                friday_fcp.innerHTML = fc_prices[data['first_courses'].indexOf(friday_fc.innerHTML)] + symbol;
                friday_scp.innerHTML = sc_prices[data['second_courses'].indexOf(friday_sc.innerHTML)] + symbol;
                friday_des_p.innerHTML = des_prices[data['desserts'].indexOf(friday_des.innerHTML)] + symbol;
                friday_dr_p.innerHTML = dr_prices[data['drinks'].indexOf(friday_dr.innerHTML)] + symbol;

                friday_fcq.innerHTML = db_data['friday']['first_course_quantity'];
                friday_scq.innerHTML = db_data['friday']['second_course_quantity'];
                friday_des_q.innerHTML = db_data['friday']['dessert_quantity'];
                friday_dr_q.innerHTML = db_data['friday']['drink_quantity'];


                let m_total = fc_prices[data['first_courses'].indexOf(monday_fc.innerHTML)] * parseInt(monday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(monday_sc.innerHTML)] * parseInt(monday_scq.innerHTML) + des_prices[data['desserts'].indexOf(monday_des.innerHTML)] * parseInt(monday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(monday_dr.innerHTML)] * monday_dr_q.innerHTML;
                let tu_total = fc_prices[data['first_courses'].indexOf(tuesday_fc.innerHTML)] * parseInt(tuesday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(tuesday_sc.innerHTML)] * parseInt(tuesday_scq.innerHTML) + des_prices[data['desserts'].indexOf(tuesday_des.innerHTML)] * parseInt(tuesday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(tuesday_dr.innerHTML)] * tuesday_dr_q.innerHTML;
                let we_total = fc_prices[data['first_courses'].indexOf(wednesday_fc.innerHTML)] * parseInt(wednesday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(wednesday_sc.innerHTML)] * parseInt(wednesday_scq.innerHTML) + des_prices[data['desserts'].indexOf(wednesday_des.innerHTML)] * parseInt(wednesday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(wednesday_dr.innerHTML)] * wednesday_dr_q.innerHTML;
                let th_total = fc_prices[data['first_courses'].indexOf(thursday_fc.innerHTML)] * parseInt(thursday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(thursday_sc.innerHTML)] * parseInt(thursday_scq.innerHTML) + des_prices[data['desserts'].indexOf(thursday_des.innerHTML)] * parseInt(thursday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(thursday_dr.innerHTML)] * thursday_dr_q.innerHTML;
                let fr_total = fc_prices[data['first_courses'].indexOf(friday_fc.innerHTML)] * parseInt(friday_fcq.innerHTML) + sc_prices[data['second_courses'].indexOf(friday_sc.innerHTML)] * parseInt(friday_scq.innerHTML) + des_prices[data['desserts'].indexOf(friday_des.innerHTML)] * parseInt(friday_des_q.innerHTML) + dr_prices[data['drinks'].indexOf(friday_dr.innerHTML)] * friday_dr_q.innerHTML;

                monday_total.innerHTML = m_total + symbol;
                tuesday_total.innerHTML = tu_total + symbol;
                wednesday_total.innerHTML = we_total + symbol;
                thursday_total.innerHTML = th_total + symbol;
                friday_total.innerHTML = fr_total + symbol;

                total.innerHTML = "Total : " + (m_total + tu_total + we_total + th_total + fr_total) + symbol;
            }
        }
    })

});
