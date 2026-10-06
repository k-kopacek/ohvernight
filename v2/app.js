'use strict';
const host=document.getElementById('app');
window.explore=ExploreShell.createShell(host,{defaultRegion:host.dataset.defaultRegion});
window.explore.start();
