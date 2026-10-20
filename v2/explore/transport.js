(function(scope){
  'use strict';

  // Keep this in lockstep with pipeline/scripts/lib/region_contract.py.
  function normalizeTransport(record){
    if(!record || typeof record!=='object' || Array.isArray(record)) return {record,used:[]};
    const result={...record};
    const used=[];
    if(Object.prototype.hasOwnProperty.call(result,'completed_at')){
      used.push('completed_at');
      if(result.last_retrieved_at===undefined) result.last_retrieved_at=result.completed_at;
      if(result.last_checked_at===undefined) result.last_checked_at=result.completed_at;
    }
    if(Object.prototype.hasOwnProperty.call(result,'retrieved_at')){
      used.push('retrieved_at');
      if(result.last_retrieved_at===undefined) result.last_retrieved_at=result.retrieved_at;
    }
    if(Object.prototype.hasOwnProperty.call(result,'checked_at')){
      used.push('checked_at');
      if(result.last_checked_at===undefined) result.last_checked_at=result.checked_at;
    }
    if(result.status==='failed'){
      used.push('failed');
      result.status='unavailable';
    }
    if(Object.prototype.hasOwnProperty.call(result,'error')){
      used.push('error');
      if(result.reason===undefined) result.reason=result.error;
    }
    if(result.status==='available' && result.last_retrieved_at===undefined && result.last_checked_at){
      used.push('inferred_retrieval');
      result.last_retrieved_at=result.last_checked_at;
    }
    if(Object.prototype.hasOwnProperty.call(result,'last_confirmed_at')) used.push('last_confirmed_at');
    if(result.last_checked_at===undefined && result.last_retrieved_at) result.last_checked_at=result.last_retrieved_at;
    return {record:result,used};
  }

  const api={normalizeTransport};
  if(typeof module!=='undefined') module.exports=api;
  scope.ExploreTransport=api;
})(typeof globalThis!=='undefined'?globalThis:this);
