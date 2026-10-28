import assert from 'node:assert/strict';
import {test} from 'node:test';
import {modulePages} from '../../runtime/frontend/src/app/modulePages.ts';

test('title/snippet outline pages use actual player scene IDs without modifying authoring data',()=>{
 const outline=[{title:'问题',snippet:'实际讲稿'},{title:'解释',snippet:'第二页讲稿'}];
 const before=JSON.stringify(outline);
 assert.deepEqual(modulePages(outline,[{id:'opening'},{id:'explain'}]),[
  {id:'opening',title:'问题',snippet:'实际讲稿'},{id:'explain',title:'解释',snippet:'第二页讲稿'}]);
 assert.equal(JSON.stringify(outline),before);
});
test('legacy stable IDs are preserved and planning-only pages remain identifiable',()=>{
 assert.equal(modulePages([{id:'kept-id',title:'已有页'}],[{id:'other'}])[0].id,'kept-id');
 assert.equal(modulePages([{title:'计划页'}])[0].id,'page-1');
 assert.deepEqual(modulePages([]),[]);
});
