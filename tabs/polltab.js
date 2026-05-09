const questions = [
  {
    text: "What age group are you in?",
    answers: ["Under 18", "18–24", "25–34", "35–44", "45+"]
  },{
    text: "Do you use AI for school or for work?",
    answers: ["Yes", "No", "Both", "Personal Use"]
  },
  {
    text: "Do you think AI has a more positive or negative affect on your life?(education/ convience/ resources)",
    answers: ["Positive", "Negative"]
  },
  {
    text: "Are you aware of any damage data centers have caused with our land, air, water?",
    answers: ["Yes", "No"]
  },{
    text: "Are you aware of people using AI as an alternative for romantic and platonic relationships?",
    answers: ["Yes", "No"]
  },{
    text: "Do you believe there will be a decline of jobs in the near future due to AI?",
    answers: ["Yes", "No", "Not sure"]
  }];

  const resultcolors = ['rgb(199, 21, 133)', 'rgb(255, 127, 80)', 'rgb(255, 215, 0)', 'rgb(106, 90, 205)', 'rgb(32, 178, 170)', 'rgb(128, 128, 0)'];

let submissions = [];
for(let i = 0; i < questions.length; i++){
  submissions.push(new Array(questions[i].answers.length).fill(0));
}
let chosen = [];
for(let i = 0; i < questions.length; i++) {
  chosen.push(null);
}

function createPoll() {
  const pollContainer = document.getElementById('poll');
  pollContainer.inHTML = '';

  for(let x = 0; x < questions.length; x++) {
    let y = questions[x];

    let box = document.createElement('div');
    box.className = 'questionblock';

    let optionsInHTML = '';
    for(let a = 0; a < y.answers.length; a++) {
      let b = y.answers[a];
      optionsInHTML += 'button class= "optionbuttons" onclick"pick(' + x + ', ' + a + ', this)">' + b + '</button>';
    }
  
