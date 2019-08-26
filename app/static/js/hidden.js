$(function() {
  // hideボタンを押したとき
  $(".open").on("click", function() {
    console.log(this)
    $(".tweet").hide();
  });
   // showボタンを押したとき
  $(".panda").on("click", function() {
    $(".tweet").show();
  });
});
