const test=require('node:test');
const assert=require('node:assert/strict');
const {fitZoomForBounds,waterMidpointMember,selectionFitAction,cappedTapCameraPlan}=require('../../explore/shell.js');

const stream={fitPolicy:{tap:{max_zoom_out:2},list:{min_zoom:11}}};
const padding={topLeft:[24,70],bottomRight:[24,120]};
const size={width:390,height:844};

test('short water line keeps the existing fit behavior and long line caps tap zoom-out',()=>{
  const short=[[-105,39],[-104.999,39.001]],long=[[-107,38],[-105,39],[-103,40]];
  const shortZoom=fitZoomForBounds([[short[0][0],short[0][1]],[short[1][0],short[1][1]]],size,padding);
  const longZoom=fitZoomForBounds([[long[0][0],long[0][1]],[long[2][0],long[2][1]]],size,padding);
  assert.equal(selectionFitAction(stream,'LineString','tap',shortZoom,shortZoom),'fit');
  assert.equal(selectionFitAction(stream,'MultiLineString','tap',14,longZoom),'tap-cap');
  assert.equal(selectionFitAction({},'LineString','tap',14,longZoom),'fit');
});

test('long water line from a list uses its minimum zoom and polygons preserve the camera',()=>{
  assert.equal(selectionFitAction(stream,'MultiLineString','list',14,8),'list-cap');
  assert.equal(selectionFitAction(stream,'MultiLineString','list',14,12),'fit');
  assert.equal(selectionFitAction(stream,'Polygon','tap',14,8),'preserve');
});

test('capped water taps preserve zoom and recenter only when the tapped point is hidden',()=>{
  const coordinate=[-105,39];
  assert.deepEqual(cappedTapCameraPlan(17,false,coordinate,size,padding),{action:'none',bounds:null,zoom:17});
  assert.deepEqual(cappedTapCameraPlan(15,true,coordinate,size,padding),{action:'none',bounds:null,zoom:15});
  const hidden=cappedTapCameraPlan(14,false,coordinate,size,padding);
  assert.equal(hidden.action,'recenter');
  assert.equal(hidden.zoom,14);
  assert.equal(fitZoomForBounds(hidden.bounds,size,padding),14);
});

test('fit zoom uses the padded viewport and midpoint follows ordered drawn geodesic length',()=>{
  const point=fitZoomForBounds([[-105,39],[-104.999,39.001]],size,padding);
  assert.ok(point>=5&&point<=15);
  const group={geometry:{type:'MultiLineString',coordinates:[
    [[-106,39],[-105,39]],
    [[-104,39],[-101,39]]
  ]}};
  const midpoint=waterMidpointMember(group);
  assert.equal(midpoint.lineIndex,1);
  assert.ok(Math.abs(midpoint.point[0]+103.0000603)<1e-6);
  assert.ok(Math.abs(midpoint.point[1]-39.0085718)<1e-6);
});
