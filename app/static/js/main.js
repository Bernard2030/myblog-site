

numberOfLike: number =0;
numberOfDislike: number=0;

likeButtonClick();{
    this.numberOfLike++;
  }
  dislikeButtonClick();{
    this.numberOfDislike--;
  }

$("p").click(function(){
    alert("The paragraph was clicked.");
  });