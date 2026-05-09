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
  pollContainer.innerHTML = '';

  for(let x = 0; x < questions.length; x++) {
    let y = questions[x];

    let box = document.createElement('div');
    box.className = 'questionbox';

    let optionsInHTML = '';
    for(let a = 0; a < y.answers.length; a++) {
      let b = y.answers[a];
      optionsInHTML += '<button class= "optionbuttons" onclick="pick(' + x + ', ' + a + ', this)">' + b + '</button>';
    }
    box.innerHTML = 
      '<div class ="questiontext">' + y.text + '</div>' + '<div class="options' + x + '">' + optionsInHTML + '</div>' + '<div class="errortext" id="error' + x + '">Select an answer before submitting. Thank you.</div>';

    pollContainer.appendChild(box);
  }
  const button = document.createElement('button');
  button.className = 'submitbutton'; 
  button.textContent = 'Submit';
  button.onclick = submit;
  pollContainer.appendChild(button);
}
function pick(x, a, button) {
  let optionGroup = document.getElementById('choices' + x);
  let allButtons = optionGroup.getElementsByClassName('optionbuttons');
  for (let i = 0; i < allButtons.length; i++) {
    allButtons[i].classList.remove('selected');
  }
  button.classList.add('selected');
  chosen[x] = a;
  document.getElementById('error' + x).style.display = 'none';
}
function submission() {
  let answered = true;
  for(x = 0; x < chosen.length; x++) {
    if(chosen[x] === null) [
      document.getElementByIdd('error' + x).style.display = 'block';
    answered = false;
  }
}
if(!answered) return;

for(let x = 0; x < chosen.length; x++){
  submissions[x][chosen[x]]++;
}
 let total = submissions[0].reduce(function(a, b) { return a + b; }, 0);

  document.getElementById('poll').style.display = 'none';
  document.getElementById('results').style.display = 'block';
  document.getElementById('totalBadge').textContent = total + ' response' + (total !== 1 ? 's' : '') + ' so far';
  createCharts();
}

function createCharts() {
  const chartContainer = document.getElementById('charts');
  chartContainer.innerHTML = '';
  for(let x = 0; x < questions.length; x++) {
    let q = questions[x];
    let s = document.createElement('div');
    s.className = "optionselect";
    s.innerHTML = 'div class="optionquestion">' + q.text + '</div><div : id="bars' + x + '"></div>';
    chartContainer.appendChild(s);
    let bd = document.getElementById('bars' + x);
    let total = 0;
    for(let i = 0; i < submissions[x].length; i++) {
      total += submissions[x][i];
    }
    for (let a = 0; a < q.answers.length; a++) {
      let counter = submissions[x][a];
      let p = 0;
      if(total > 0) {
        p = Math.rounf((counter / total) * 100);
      }
      let r = document.createElement('div');
      r.className = 'row';
      r.innerHTML = '<div class="blabel">' + q.answers[a] + '</div>' + '<div class="btrack"><div class="bfill" style="width:' + pct + '%;background:' + resultcolors[a % resultcolors.length] + '"></div></div>' + '<div class="bpct">' + pct + '%</div>';
      barsDiv.appendChild(r);
    }
  }
}
    
  
