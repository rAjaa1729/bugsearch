// Get references to the upvote and downvote buttons
const upvoteBtn=document.getElementById('upvote-btn');
const downvoteBtn=document.getElementById('downvote-btn');


// Add event listeners to the buttons
upvoteBtn.addEventListener('click',updateupvote());

function updateupvote()
{
    console.log('has entered in the upvote function upvote clicked ');
    const xhr=new XMLHttpRequest();

    xhr.open('GET','/updatevote',true);

    xhr.onload = function()
    {
        if(this.status===200)
        {
        console.log("has clicked and request has been sent");
        }
        else
        {
            console.log("request not send ")
        }
    }
    xhr.send();
}

// upvoteBtn.addEventListener('click', () => {
//   if (upvoteBtn.classList.contains('selected')) {
//     // User has already upvoted, so remove their vote
//     upvoteBtn.classList.remove('selected');
//     upvotes--;
//   } else {
//     // User is upvoting for the first time
//     upvoteBtn.classList.add('selected');
//     downvoteBtn.classList.remove('selected');
//     upvotes++;

//     // If the user has already downvoted, remove their vote
//     if (downvotes > 0) {
//       downvotes--;
//     }
//   }

//   // Update the UI with the new vote counts
//   updateVoteCounts();
// });

// downvoteBtn.addEventListener('click', () => {
//   if (downvoteBtn.classList.contains('selected')) {
//     // User has already downvoted, so remove their vote
//     downvoteBtn.classList.remove('selected');
//     downvotes--;
//   } else {
//     // User is downvoting for the first time
//     downvoteBtn.classList.add('selected');
//     upvoteBtn.classList.remove('selected');
//     downvotes++;

//     // If the user has already upvoted, remove their vote
//     if (upvotes > 0) {
//       upvotes--;
//     }
//   }

//   // Update the UI with the new vote counts
//   updateVoteCounts();
// });

// function updateVoteCounts() {
//   const upvoteCount = document.getElementById('upvote-count');
//   const downvoteCount = document.getElementById('downvote-count');

//   upvoteCount.innerText = upvotes.toString();
//   downvoteCount.innerText = downvotes.toString();
// }


// function updateVoteCounts()
// {

// }