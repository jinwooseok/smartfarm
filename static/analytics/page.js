const $ls = document.querySelector('#listset');
const $list1 = document.querySelector('#list1');
const $list2 = document.querySelector('#list2');
const $list3 = document.querySelector('#list3');
const $list4 = document.querySelector('#list4');
const $list5 = document.querySelector('#list5');
const $ex1 = document.querySelector('#ex1');
const $ex2 = document.querySelector('#ex2');
const $ex3 = document.querySelector('#ex3');
const $ex4 = document.querySelector('#ex4');
const $ex5 = document.querySelector('#ex5');


$ls.addEventListener('click', (event)=>{
    event.preventDefault();
    if (event.target.textContent==='graph'){
        // 색상
        $list1.style.backgroundColor='blue';
        $list1.style.color='white';
        $list2.style.backgroundColor='white';
        $list2.style.color='black';
        $list3.style.backgroundColor='white';
        $list3.style.color='black';
        $list4.style.backgroundColor='white';
        $list4.style.color='black';
        $list5.style.backgroundColor='white';
        $list5.style.color='black';

        // div
        $ex1.style.display='block';
        $ex2.style.display='none';
        $ex3.style.display='none';
        $ex4.style.display='none';
        $ex5.style.display='none';
    } 
    
    else if(event.target.textContent==='summary'){
        $list2.style.backgroundColor='blue';
        $list2.style.color='white';
        $list1.style.backgroundColor='white';
        $list1.style.color='black';
        $list3.style.backgroundColor='white';
        $list3.style.color='black';
        $list4.style.backgroundColor='white';
        $list4.style.color='black';
        $list5.style.backgroundColor='white';
        $list5.style.color='black';

        // div
        $ex1.style.display='none';
        $ex2.style.display='block';
        $ex3.style.display='none';
        $ex4.style.display='none';
        $ex5.style.display='none';
    } 
    
    else if(event.target.textContent==='analytics'){
        $list3.style.backgroundColor='blue';
        $list3.style.color='white';
        $list1.style.backgroundColor='white';
        $list1.style.color='black';
        $list2.style.backgroundColor='white';
        $list2.style.color='black';
        $list4.style.backgroundColor='white';
        $list4.style.color='black';
        $list5.style.backgroundColor='white';
        $list5.style.color='black';

        // div
        $ex1.style.display='none';
        $ex2.style.display='none';
        $ex3.style.display='block';
        $ex4.style.display='none';
        $ex5.style.display='none';
    } 
    
    else if(event.target.textContent==='ml'){
        $list4.style.backgroundColor='blue';
        $list4.style.color='white';
        $list1.style.backgroundColor='white';
        $list1.style.color='black';
        $list2.style.backgroundColor='white';
        $list2.style.color='black';
        $list3.style.backgroundColor='white';
        $list3.style.color='black';
        $list5.style.backgroundColor='white';
        $list5.style.color='black';

        // div
        $ex1.style.display='none';
        $ex2.style.display='none';
        $ex3.style.display='none';
        $ex4.style.display='block';
        $ex5.style.display='none';
    }

    else if(event.target.textContent==='농업전처리'){
        $list5.style.backgroundColor='blue';
        $list5.style.color='white';
        $list1.style.backgroundColor='white';
        $list1.style.color='black';
        $list2.style.backgroundColor='white';
        $list2.style.color='black';
        $list3.style.backgroundColor='white';
        $list3.style.color='black';
        $list4.style.backgroundColor='white';
        $list4.style.color='black';

        // div
        $ex1.style.display='none';
        $ex2.style.display='none';
        $ex3.style.display='none';
        $ex4.style.display='none';
        $ex5.style.display='block';
    }
});


