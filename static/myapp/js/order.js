let list = document.getElementsByClassName('list');
let currentid = 1;
let first = document.getElementById('first');
let second = document.getElementById('second');
let third = document.getElementById('third');
let four = document.getElementById('four');
let five = document.getElementById('five');
let all = [first,second,third,four,five];
let save = document.getElementById('save');
let next = document.getElementById('next');
let x;
let l;
let m;
let grn = document.getElementById('grn');
let grn2 = document.getElementById('grn2');
let grn3 = document.getElementById('grn3');
let grn4 = document.getElementById('grn4');
let grn5 = document.getElementById('grn5');
let mny = [grn,grn2,grn3,grn4,grn5]

function activeList(){
    for(l of list){
        l.classList.remove("active");
    }
    event.target.classList.add("active");
    currentid = event.target.id;
    console.log(currentid);
    for(x of all){
        x.classList.add('off');
        for(m of mny){
            m.classList.add('off');
            if(currentid == 1){
                x.classList.remove('on');
                first.classList.add('on');
                save.style.visibility = 'hidden';
                grn.classList.remove('off');
            } else if(currentid == 2){
                x.classList.remove('on');
                second.classList.add('on');
                save.style.visibility = 'hidden';
                grn2.classList.remove('off');
            } else if(currentid == 3){
                x.classList.remove('on');
                third.classList.add('on');
                save.style.visibility = 'hidden';
                grn3.classList.remove('off');
            } else if(currentid == 4){
                x.classList.remove('on');
                four.classList.add('on');
                save.style.visibility = 'hidden';
                grn4.classList.remove('off');
            } else if(currentid == 5){
                x.classList.remove('on');
                five.classList.add('on');
                save.style.visibility = 'visible';
                grn5.classList.remove('off');
            }}}}

let data;
$(document).ready(function(){

    $.ajax({
        type: 'GET',
        url: "/set_price/",
        success: function(response){
            data = response['response'];
        }
    })
    
});

let f1_fc_price = document.getElementById('f1_fcp');
let f1_fcq = document.getElementById('f1_fcq');
$('#f1_fc').on('change', function(){
    let f1_fc_prices = data['first_course_prices']; 
    let f1_fc_val = $('#f1_fc').val(); 
    let f1_fc_idx = data['first_courses'].indexOf(f1_fc_val);
    f1_fc_price.innerHTML = f1_fc_prices[f1_fc_idx];
    $('#f1_fcq').val(0);
});

let f1_sc_price = document.getElementById('f1_scp');
let f1_scq = document.getElementById('f1_scq');
$('#f1_sc').on('change', function(){
    let f1_sc_prices = data['second_course_prices']; 
    let f1_sc_val = $('#f1_sc').val(); 
    let f1_sc_idx = data['second_courses'].indexOf(f1_sc_val);
    f1_sc_price.innerHTML = f1_sc_prices[f1_sc_idx];
    $('#f1_scq').val(0);
});


let f1_des_price = document.getElementById('f1_des_p');
let f1_des_q = document.getElementById('f1_des_q');
$('#f1_des').on('change', function(){
    let f1_des_prices = data['dessert_prices']; 
    let f1_des_val = $('#f1_des').val(); 
    let f1_des_idx = data['desserts'].indexOf(f1_des_val);
    f1_des_price.innerHTML = f1_des_prices[f1_des_idx];
    $('#f1_des_q').val(0);
});


let f1_dr_price = document.getElementById('f1_dr_p');
let f1_dr_q = document.getElementById('f1_dr_q');
$('#f1_dr').on('change', function(){
    let f1_dr_prices = data['drinks_prices']; 
    let f1_dr_val = $('#f1_dr').val(); 
    let f1_dr_idx = data['drinks'].indexOf(f1_dr_val);
    f1_dr_price.innerHTML = f1_dr_prices[f1_dr_idx];
    $('#f1_dr_q').val(0);
});



let f2_fc_price = document.getElementById('f2_fcp');
let f2_fcq = document.getElementById('f2_fcq');
$('#f2_fc').on('change', function(){
    let f2_fc_prices = data['first_course_prices']; 
    let f2_fc_val = $('#f2_fc').val(); 
    let f2_fc_idx = data['first_courses'].indexOf(f2_fc_val);
    f2_fc_price.innerHTML = f2_fc_prices[f2_fc_idx];
    $('#f2_fcq').val(0);
});

let f2_sc_price = document.getElementById('f2_scp');
let f2_scq = document.getElementById('f2_scq');
$('#f2_sc').on('change', function(){
    let f2_sc_prices = data['second_course_prices']; 
    let f2_sc_val = $('#f2_sc').val(); 
    let f2_sc_idx = data['second_courses'].indexOf(f2_sc_val);
    f2_sc_price.innerHTML = f2_sc_prices[f2_sc_idx];
    $('#f2_scq').val(0);
});


let f2_des_price = document.getElementById('f2_des_p');
let f2_des_q = document.getElementById('f2_des_q');
$('#f2_des').on('change', function(){
    let f2_des_prices = data['dessert_prices']; 
    let f2_des_val = $('#f2_des').val(); 
    let f2_des_idx = data['desserts'].indexOf(f2_des_val);
    f2_des_price.innerHTML = f2_des_prices[f2_des_idx];
    $('#f2_des_q').val(0);
});


let f2_dr_price = document.getElementById('f2_dr_p');
let f2_dr_q = document.getElementById('f2_dr_q');
$('#f2_dr').on('change', function(){
    let f2_dr_prices = data['drinks_prices']; 
    let f2_dr_val = $('#f2_dr').val(); 
    let f2_dr_idx = data['drinks'].indexOf(f2_dr_val);
    f2_dr_price.innerHTML = f2_dr_prices[f2_dr_idx];
    $('#f2_dr_q').val(0);
});


let f3_fc_price = document.getElementById('f3_fcp');
let f3_fcq = document.getElementById('f3_fcq');
$('#f3_fc').on('change', function(){
    let f3_fc_prices = data['first_course_prices']; 
    let f3_fc_val = $('#f3_fc').val(); 
    let f3_fc_idx = data['first_courses'].indexOf(f3_fc_val);
    f3_fc_price.innerHTML = f3_fc_prices[f3_fc_idx];
    $('#f3_fcq').val(0);
});

let f3_sc_price = document.getElementById('f3_scp');
let f3_scq = document.getElementById('f3_scq');
$('#f3_sc').on('change', function(){
    let f3_sc_prices = data['second_course_prices']; 
    let f3_sc_val = $('#f3_sc').val(); 
    let f3_sc_idx = data['second_courses'].indexOf(f3_sc_val);
    f3_sc_price.innerHTML = f3_sc_prices[f3_sc_idx];
    $('#f3_scq').val(0);
});


let f3_des_price = document.getElementById('f3_des_p');
let f3_des_q = document.getElementById('f3_des_q');
$('#f3_des').on('change', function(){
    let f3_des_prices = data['dessert_prices']; 
    let f3_des_val = $('#f3_des').val(); 
    let f3_des_idx = data['desserts'].indexOf(f3_des_val);
    f3_des_price.innerHTML = f3_des_prices[f3_des_idx];
    $('#f3_des_q').val(0);
});


let f3_dr_price = document.getElementById('f3_dr_p');
let f3_dr_q = document.getElementById('f3_dr_q');
$('#f3_dr').on('change', function(){
    let f3_dr_prices = data['drinks_prices']; 
    let f3_dr_val = $('#f3_dr').val(); 
    let f3_dr_idx = data['drinks'].indexOf(f3_dr_val);
    f3_dr_price.innerHTML = f3_dr_prices[f3_dr_idx];
    $('#f3_dr_q').val(0);
});


let f4_fc_price = document.getElementById('f4_fcp');
let f4_fcq = document.getElementById('f4_fcq');
$('#f4_fc').on('change', function(){
    let f4_fc_prices = data['first_course_prices']; 
    let f4_fc_val = $('#f4_fc').val(); 
    let f4_fc_idx = data['first_courses'].indexOf(f4_fc_val);
    f4_fc_price.innerHTML = f4_fc_prices[f4_fc_idx];
    $('#f4_fcq').val(0);
});

let f4_sc_price = document.getElementById('f4_scp');
let f4_scq = document.getElementById('f4_scq');
$('#f4_sc').on('change', function(){
    let f4_sc_prices = data['second_course_prices']; 
    let f4_sc_val = $('#f4_sc').val(); 
    let f4_sc_idx = data['second_courses'].indexOf(f4_sc_val);
    f4_sc_price.innerHTML = f4_sc_prices[f4_sc_idx];
    $('#f4_scq').val(0);
});

let f4_des_price = document.getElementById('f4_des_p');
let f4_des_q = document.getElementById('f4_des_q');
$('#f4_des').on('change', function(){
    let f4_des_prices = data['dessert_prices']; 
    let f4_des_val = $('#f4_des').val(); 
    let f4_des_idx = data['desserts'].indexOf(f4_des_val);
    f4_des_price.innerHTML = f4_des_prices[f4_des_idx];
    $('#f4_des_q').val(0);
});

let f4_dr_price = document.getElementById('f4_dr_p');
let f4_dr_q = document.getElementById('f4_dr_q');
$('#f4_dr').on('change', function(){
    let f4_dr_prices = data['drinks_prices']; 
    let f4_dr_val = $('#f4_dr').val(); 
    let f4_dr_idx = data['drinks'].indexOf(f4_dr_val);
    f4_dr_price.innerHTML = f4_dr_prices[f4_dr_idx];
    $('#f4_dr_q').val(0);
});


let f5_fc_price = document.getElementById('f5_fcp');
let f5_fcq = document.getElementById('f5_fcq');
$('#f5_fc').on('change', function(){
    let f5_fc_prices = data['first_course_prices']; 
    let f5_fc_val = $('#f5_fc').val(); 
    let f5_fc_idx = data['first_courses'].indexOf(f5_fc_val);
    f5_fc_price.innerHTML = f5_fc_prices[f5_fc_idx]; 
    $('#f5_fcq').val(0);
});

let f5_sc_price = document.getElementById('f5_scp');
let f5_scq = document.getElementById('f5_scq');
$('#f5_sc').on('change', function(){
    let f5_sc_prices = data['second_course_prices']; 
    let f5_sc_val = $('#f5_sc').val(); 
    let f5_sc_idx = data['second_courses'].indexOf(f5_sc_val);
    f5_sc_price.innerHTML = f5_sc_prices[f5_sc_idx];
    $('#f5_scq').val(0);
});

let f5_des_price = document.getElementById('f5_des_p');
let f5_des_q = document.getElementById('f5_des_q');
$('#f5_des').on('change', function(){
    let f5_des_prices = data['dessert_prices']; 
    let f5_des_val = $('#f5_des').val(); 
    let f5_des_idx = data['desserts'].indexOf(f5_des_val);
    f5_des_price.innerHTML = f5_des_prices[f5_des_idx];
    $('#f5_des_q').val(0);
});

let f5_dr_price = document.getElementById('f5_dr_p');
let f5_dr_q = document.getElementById('f5_dr_q');
$('#f5_dr').on('change', function(){
    let f5_dr_prices = data['drinks_prices']; 
    let f5_dr_val = $('#f5_dr').val(); 
    let f5_dr_idx = data['drinks'].indexOf(f5_dr_val);
    f5_dr_price.innerHTML = f5_dr_prices[f5_dr_idx];
    $('#f5_dr_q').val(0);
});


let symbol = " €";


function get_values_f1() {
    return {
        "fc_quantity": $('#f1_fcq').val(),
        "sc_quantity": $('#f1_scq').val(),
        "des_quantity": $('#f1_des_q').val(),
        "dr_quantity": $('#f1_dr_q').val(),
        "fc_prices": data['first_course_prices'],
        "fc_idx": data['first_courses'].indexOf($('#f1_fc').val()),
        "sc_prices": data['second_course_prices'],
        "sc_idx": data['second_courses'].indexOf($('#f1_sc').val()),
        "des_prices": data['dessert_prices'],
        "des_idx": data['desserts'].indexOf($('#f1_des').val()),
        "dr_prices": data['drinks_prices'],
        "dr_idx": data['drinks'].indexOf($('#f1_dr').val())
    }  
};


$('#f1_fcq').on('change', function(){
    
    let values = get_values_f1();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f1_scq').on('change', function(){
    
    let values = get_values_f1();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f1_des_q').on('change', function(){
    
    let values = get_values_f1();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f1_dr_q').on('change', function(){
    
    let values = get_values_f1();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


// -----------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------

function get_values_f2() {
    return {
        "fc_quantity": $('#f2_fcq').val(),
        "sc_quantity": $('#f2_scq').val(),
        "des_quantity": $('#f2_des_q').val(),
        "dr_quantity": $('#f2_dr_q').val(),
        "fc_prices": data['first_course_prices'],
        "fc_idx": data['first_courses'].indexOf($('#f2_fc').val()),
        "sc_prices": data['second_course_prices'],
        "sc_idx": data['second_courses'].indexOf($('#f2_sc').val()),
        "des_prices": data['dessert_prices'],
        "des_idx": data['desserts'].indexOf($('#f2_des').val()),
        "dr_prices": data['drinks_prices'],
        "dr_idx": data['drinks'].indexOf($('#f2_dr').val())
    }  
};


$('#f2_fcq').on('change', function(){
    
    let values = get_values_f2();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn2');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f2_scq').on('change', function(){
    
    let values = get_values_f2();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn2');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f2_des_q').on('change', function(){
    
    let values = get_values_f2();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn2');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f2_dr_q').on('change', function(){
    
    let values = get_values_f2();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn2');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});



// -----------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------

function get_values_f3() {
    return {
        "fc_quantity": $('#f3_fcq').val(),
        "sc_quantity": $('#f3_scq').val(),
        "des_quantity": $('#f3_des_q').val(),
        "dr_quantity": $('#f3_dr_q').val(),
        "fc_prices": data['first_course_prices'],
        "fc_idx": data['first_courses'].indexOf($('#f3_fc').val()),
        "sc_prices": data['second_course_prices'],
        "sc_idx": data['second_courses'].indexOf($('#f3_sc').val()),
        "des_prices": data['dessert_prices'],
        "des_idx": data['desserts'].indexOf($('#f3_des').val()),
        "dr_prices": data['drinks_prices'],
        "dr_idx": data['drinks'].indexOf($('#f3_dr').val())
    }  
};


$('#f3_fcq').on('change', function(){
    
    let values = get_values_f3();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn3');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f3_scq').on('change', function(){
    
    let values = get_values_f3();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn3');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f3_des_q').on('change', function(){
    
    let values = get_values_f3();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn3');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f3_dr_q').on('change', function(){
    
    let values = get_values_f3();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn3');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});



// -----------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------

function get_values_f4() {
    return {
        "fc_quantity": $('#f4_fcq').val(),
        "sc_quantity": $('#f4_scq').val(),
        "des_quantity": $('#f4_des_q').val(),
        "dr_quantity": $('#f4_dr_q').val(),
        "fc_prices": data['first_course_prices'],
        "fc_idx": data['first_courses'].indexOf($('#f4_fc').val()),
        "sc_prices": data['second_course_prices'],
        "sc_idx": data['second_courses'].indexOf($('#f4_sc').val()),
        "des_prices": data['dessert_prices'],
        "des_idx": data['desserts'].indexOf($('#f4_des').val()),
        "dr_prices": data['drinks_prices'],
        "dr_idx": data['drinks'].indexOf($('#f4_dr').val())
    }  
};


$('#f4_fcq').on('change', function(){
    
    let values = get_values_f4();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn4');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f4_scq').on('change', function(){
    
    let values = get_values_f4();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn4');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f4_des_q').on('change', function(){
    
    let values = get_values_f4();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn4');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f4_dr_q').on('change', function(){
    
    let values = get_values_f4();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn4');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});



// -----------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------

function get_values_f5() {
    return {
        "fc_quantity": $('#f5_fcq').val(),
        "sc_quantity": $('#f5_scq').val(),
        "des_quantity": $('#f5_des_q').val(),
        "dr_quantity": $('#f5_dr_q').val(),
        "fc_prices": data['first_course_prices'],
        "fc_idx": data['first_courses'].indexOf($('#f5_fc').val()),
        "sc_prices": data['second_course_prices'],
        "sc_idx": data['second_courses'].indexOf($('#f5_sc').val()),
        "des_prices": data['dessert_prices'],
        "des_idx": data['desserts'].indexOf($('#f5_des').val()),
        "dr_prices": data['drinks_prices'],
        "dr_idx": data['drinks'].indexOf($('#f5_dr').val())
    }  
};


$('#f5_fcq').on('change', function(){
    
    let values = get_values_f5();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn5');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f5_scq').on('change', function(){
    
    let values = get_values_f5();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn5');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f5_des_q').on('change', function(){
    
    let values = get_values_f5();

    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn5');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});


$('#f5_dr_q').on('change', function(){
    
    let values = get_values_f5();
    $.ajax({
        type:'POST',
        url: '/set_total_price/',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
        },
        data: {
            'fc_quantity': values['fc_quantity'],
            'fc_price': values['fc_prices']['' + values['fc_idx']],
            'sc_quantity': values['sc_quantity'],
            'sc_price': values['sc_prices']['' + values['sc_idx']],
            'des_quantity': values['des_quantity'],
            'des_price': values['des_prices']['' + values['des_idx']],
            'dr_quantity': values['dr_quantity'],
            'dr_price': values['dr_prices']['' + values['dr_idx']]
        },
        success: function(response){
            let tm = document.getElementById('grn5');
            tm.innerHTML = response['response'] + symbol;
            if (response['deducted_amount'] == true){
                alert("Warning! The amount of your order exceeds 20 euros. The difference will be " +
                "deducted from your salary.")
            };
        }
      
    })
});

