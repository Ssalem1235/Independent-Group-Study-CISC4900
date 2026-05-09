import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getDatabase, ref, update, get } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-database.js";

const firebaseConfig = {
  databaseURL: "https://aiimpactproject-ecad5-default-rtdb.firebaseio.com"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

const questions = [
  {
    text: "What age group are you in?",
    answers: ["Under 18", "18–24", "25–34", "35–44", "45+"]
  },
  {
    text: "Do you use AI for school or for work?",
    answers: ["Yes", "No", "Both", "Personal Use"]
  },
  {
    text: "Do you think AI has a more positive or negative affect on your life? (education / convenience / resources)",
    answers: ["Positive", "Negative"]
  },
  {
    text: "Are you aware of any damage data centers have caused with our land, air, water?",
    answers: ["Yes", "No"]
  },
  {
    text: "Are you aware of people using AI as an alternative for romantic and platonic relationships?",
    answers: ["Yes", "No"]
  },
  {
    text: "Do you believe there will be a decline of jobs in the near future due to AI?",
    answers: ["Yes", "No", "Not sure"]
  }
];

const resultcolors = ['rgb(199, 21, 133)', 'rgb(255, 127, 80)', 'rgb(255, 215, 0)', 'rgb(106, 90, 205)', 'rgb(32, 178, 170)', 'rgb(128, 128, 0)'];

let chosen = [];
for (let i = 0; i < questions.length; i++) {
  chosen.push(null);
}

function createPoll() {
  const pollContainer = document.getElementById('poll');
  pollContainer.innerHTML = '';

  for (let x = 0; x < questions.length; x++) {
    let y = questions[x];
    let box = document.createElement('div');
    box.className = 'questionbox';

    let optionsDiv = document.createElement('div');
    optionsDiv.className = 'options';
    optionsDiv.id = 'options' + x;

    for (let a = 0; a < y.answers.length; a++) {
      let btn = document.createElement('button');
      btn.className = 'optionbuttons';
      btn.textContent = y.answers[a];
      btn.addEventListener('click', function() {
        pick(x, a, btn);
      });
      optionsDiv.appendChild(btn);
    }

    let questionText = document.createElement('div');
    questionText.className = 'questiontext';
    questionText.textContent = y.text;

    let errorText = document.createElement('div');
    errorText.className = 'errortext';
    errorText.id = 'error' + x;
    errorText.textContent = 'Please select an answer before submitting.';
    errorText.style.display = 'none';

    box.appendChild(questionText);
    box.appendChild(optionsDiv);
    box.appendChild(errorText);
    pollContainer.appendChild(box);
  }

  const button = document.createElement('button');
  button.className = 'submitbutton';
  button.textContent = 'Submit';
  button.addEventListener('click', submission);
  pollContainer.appendChild(button);
}

function pick(x, a, button) {
  let optionGroup = document.getElementById('options' + x);
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
  for (let x = 0; x < chosen.length; x++) {
    if (chosen[x] === null) {
      document.getElementById('error' + x).style.display = 'block';
      answered = false;
    }
  }
  if (!answered) return;

  const pollRef = ref(db, 'pollResults');
  get(pollRef).then(function(snapshot) {
    let current = {};
    if (snapshot.exists()) {
      current = snapshot.val();
    }

    let updates = {};
    for (let x = 0; x < questions.length; x++) {
      let answerIndex = chosen[x];
      let key = 'q' + x + '_a' + answerIndex;
      updates[key] = (current[key] || 0) + 1;
    }

    let totalKey = 'totalSubmissions';
    updates[totalKey] = (current[totalKey] || 0) + 1;

    update(pollRef, updates).then(function() {
      localStorage.setItem('hasSubmitted', 'true');
      document.getElementById('poll').style.display = 'none';
      document.getElementById('results').style.display = 'block';
      loadAndShowCharts();
    });
  });
}

function loadAndShowCharts() {
  const pollRef = ref(db, 'pollResults');
  get(pollRef).then(function(snapshot) {
    let data = {};
    if (snapshot.exists()) {
      data = snapshot.val();
    }
    let total = data['totalSubmissions'] || 0;
    document.getElementById('totalCount').textContent = total + ' responses so far';
    createCharts(data);
  });
}

function createCharts(data) {
  const chartContainer = document.getElementById('charts');
  chartContainer.innerHTML = '';

  for (let x = 0; x < questions.length; x++) {
    let q = questions[x];
    let s = document.createElement('div');
    s.className = 'optionselect';
    s.innerHTML = '<div class="optionquestion">' + q.text + '</div><div id="bars' + x + '"></div>';
    chartContainer.appendChild(s);
    let bd = document.getElementById('bars' + x);

    let qTotal = 0;
    for (let a = 0; a < q.answers.length; a++) {
      qTotal += (data['q' + x + '_a' + a] || 0);
    }

    for (let a = 0; a < q.answers.length; a++) {
      let count = data['q' + x + '_a' + a] || 0;
      let p = 0;
      if (qTotal > 0) {
        p = Math.round((count / qTotal) * 100);
      }
      let r = document.createElement('div');
      r.className = 'countrow';
      r.innerHTML =
        '<div class="countlabel">' + q.answers[a] + '</div>' +
        '<div class="counttrack"><div class="countfill" style="width:' + p + '%;background:' + resultcolors[a % resultcolors.length] + '"></div></div>' +
        '<div class="countp">' + p + '%</div>';
      bd.appendChild(r);
    }
  }
}

if (localStorage.getItem('hasSubmitted') === 'true') {
  document.getElementById('poll').style.display = 'none';
  document.getElementById('results').style.display = 'block';
  loadAndShowCharts();
} else {
  createPoll();
}
