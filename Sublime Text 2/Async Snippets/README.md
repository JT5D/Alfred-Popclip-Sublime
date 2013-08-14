# Sublime Text 2 Async-Snippets

This package contains Sublime Text 2 snippets to be used with the [Async .js utility](https://github.com/caolan/async).

In order to use the snippets, enter the shortcode and press <kbd>Tab</kbd> (or whatever you have set as completion key).

Included are all snippets listed below. $1, $2, etc. show the position where the caret will appear whenever you press the tab key inside the snippet.

---

__async_foreach__

```js
async.forEach(
  ${1:array}, 
  function(item,callback){
    ${2:callback();}
  }, 
  function(err){
    // if any of the saves produced an error, err would equal that error
    if(err){
      ${3}
    }else{
      ${4}
    }
  }
);
```

__async_parallel__

```js
async.parallel({
    ${1:one}: function(callback){
        ${2://body}
    },
    ${3:two}: function(callback){
        ${4://body}
    },
},
function(err, ${5:results}) {
    // results now equals: {one: 1, two: 2}
    $6
});
```

__async_series__

```js
async.series({
  ${1:one}: function(callback){
      ${2:callback(null,{})}
  },
  ${3:two}: function(callback){
      ${4:callback(null,{})}
  },
},
function(err, ${5:results}) {
  // results is now equal to: {one: 1, two: 2}
  ${6}
});
```

__async_waterfall__

```js
async.waterfall([
  function(callback){
      callback(null, ${1:'one'}, ${2:'two'});
  },
  function(${3:arg1}, ${4:arg2}, callback){
      callback(null, ${5:'three'});
  },
  function(${6:arg1}, callback){
      // arg1 now equals 'three'
      callback(null, ${7:'done'});
  }
], function (err, ${8:result}) {
  // result now equals 'done'    
});
```
