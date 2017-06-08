/**
 *   Main JS file. Javascript to be used throughout the page.
 */

/**
 *   Navigation trigger behavior
 *   Relies on element.classList --> IE > v.10
 */

var trigger = document.querySelector('.trigger-navigation');

trigger.addEventListener('click', function(){
    var header = document.querySelector('.region-header');
    header.classList.toggle('region-header--unfolded');
});
