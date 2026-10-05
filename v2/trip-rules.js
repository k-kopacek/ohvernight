(function (scope) {
  function parseDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return null;
    const date = new Date(value + 'T00:00:00Z');
    return Number.isFinite(+date) && date.toISOString().slice(0,10) === value ? date : null;
  }
  function tripDays(arrive, depart) {
    const first = parseDate(arrive), last = parseDate(depart);
    if (!first || !last || last <= first || last-first > 366*86400000) return null;
    const days = [];
    for (let day=+first; day<=+last; day+=86400000) days.push(new Date(day).toISOString().slice(5));
    return days;
  }
  function evaluate(place, trip, today=new Date().toISOString().slice(0,10), policy) {
    const days=tripDays(trip.arrive,trip.depart);
    let result={...place,status:'review',label:'Needs trip review',tripNote:'Access, overnight permission and availability need confirmation.'};
    if (!days) return {...result,label:'Enter valid trip dates',tripNote:'Choose a stay of 1–366 nights.'};
    const checked=parseDate(place.checked_on), current=parseDate(today);
    const maxAgeHours=policy?.max_age_hours;
    const stale=!checked || !current || current<checked ||
      !Number.isFinite(maxAgeHours) || maxAgeHours<=0 || current-checked>maxAgeHours*3600000;
    const finish=fresh=>{
      if (!stale) return {...fresh,sourceStale:false};
      if (fresh.status==='excluded' || fresh.label==='Motorhome suitability unverified')
        return {...fresh,tripNote:fresh.tripNote+' The source review is out of date; recheck the linked sources before travel.',sourceStale:true};
      return {...fresh,label:'Source review is stale',tripNote:'Recheck the linked sources before relying on previous setup or access notes.',sourceStale:true};
    };
    const stayLimit=Number(place.stay_limit_days ?? place.max_stay_days);
    if (Number.isFinite(stayLimit) && stayLimit > 0 && days.length-1 > stayLimit)
      return finish({...result,status:'excluded',label:'Stay exceeds published limit',tripNote:`This area lists a maximum stay of ${stayLimit} days. Shorten the trip or choose a different overnight option.`});
    if (place.kind==='lodging') return finish({...result,label:'Room backup · check availability',tripNote:'Book a room with the operator. This is not permission to sleep in the parking lot.'});
    if (place.tent_only) return finish({...result,status:'excluded',label:'Tent-only · vehicle-sleeping mismatch',tripNote:'The published sites are walk-in and tent-only.'});
    if (place.requires_high_clearance && trip.vehicle==='passenger_car')
      return finish({...result,status:'excluded',label:'High clearance required',tripNote:'The agency specifies high clearance. Passenger-car access does not meet that requirement.'});
    if (place.access) {
      const designation=place.access.designations[trip.vehicle];
      // Only accept the agency's exact MM/DD-MM/DD interval format.
      const intervals=(designation?.dates_open || '').split(/[;,]/).map(v=>v.trim().match(/^(\d{2}\/\d{2})-(\d{2}\/\d{2})$/));
      const valid=designation?.designation==='open' && intervals.length && intervals.every(m=>m && parseDate('2000-'+m[1].replace('/','-')) && parseDate('2000-'+m[2].replace('/','-')));
      if (valid && !days.every(day=>intervals.some(m=>{const a=m[1].replace('/','-'),b=m[2].replace('/','-');return a<=b ? day>=a&&day<=b : day>=a||day<=b;})))
        return finish({...result,status:'excluded',label:'Outside mapped vehicle-access season',tripNote:'At least one trip day, including departure, falls outside the published designation for the campground road. This is a road-access check, not a campground operating calendar.'});
      if (valid) result.tripNote='Within the mapped campground-road designation. Full approach, current conditions, sleeping setup, operating dates and availability still need confirmation.';
    }
    if (place.requires_high_clearance && trip.vehicle==='motorhome')
      return finish({...result,label:'Motorhome suitability unverified',tripNote:'High clearance is required; motorhome dimensions and suitability have not been checked.'});
    if (place.kind==='dispersed') result.label='Dispersed area · access unverified';
    return finish(result);
  }
  const api={evaluate,tripDays};
  if (typeof module!=='undefined') module.exports=api;
  scope.TripRules=api;
})(typeof globalThis!=='undefined'?globalThis:this);
