/**
 * Title: Quiz App
 * Description: Generate some quizes with answer form another server.
 * Author: Samin Yasar
 * Date: 20/August/2021
 */
//These lines select various HTML elements by their IDs and assign them
// to corresponding variables. These variables will be used to interact with
// the DOM (Document Object Model) and display quiz-related information
// DOM Select
const quizTopicSpan = document.getElementById("quizTopicSpan");
const quizNumberEl = document.getElementById("quizNumberEl");
const quizIncorrectSpan = document.getElementById("quizIncorrectSpan");
const quizCorrectSpan = document.getElementById("quizCorrectSpan");
const countdownTimeBar = document.getElementById("countdownTimeBar");
const quizQuestionEl = document.getElementById("quizQuestionEl");
const quizOptionListEl = document.getElementById("quizOptionListEl");
const quizControls = document.getElementById("quizControls");

// Here, global variables are defined to store various aspects 
// of the quiz, such as the number of quizzes, time limits, pass mark percentage,
//  and variables to keep track of time, 
// current quiz number, incorrect and correct answers, and other related data.

// Global Variables

const quizAmount = 20;
const timePerQuiz = 10;
const passMark = 70; // ! in percentage
let totalTime = quizAmount * timePerQuiz;
let currentTime = totalTime;
let currentQuiz = 1;
let countIncorrect = (countCorrect = 0);
let nextQuestion = null;
let intervalId = null;

const correctAnswers = [];
const answers = [];
// Here, global variables are defined to store various aspects of 
// the quiz, such as the number of quizzes, time limits, 
// pass mark percentage, and variables to keep track of time, 
// current quiz number, incorrect and correct answers, and other related data.

const quizCategories = {
    nature: 17,
    computers: 18,
    mathematics: 19,
    sports: 21,
    animals: 27,
    gadgets: 30,
};
//This code randomly selects a quiz category from quizCategories by generating 
//a random index within the range of available categories.
const quizTopic =
    Object.keys(quizCategories)[
        Math.floor(Math.random() * Object.keys(quizCategories).length)
    ];
//This line assigns the numerical ID of the selected quiz category to quizCategoryId.
// This ID will be 
//used when making API requests to fetch questions for the selected category.
const quizCategoryId = quizCategories[quizTopic];
//These lines define an array of quiz difficulties ("easy," "medium," and "hard")
// and randomly select a difficulty level to
// use when fetching questions.
const quizDifficulties = ["easy", "medium", "hard"];
const quizDifficulty =
    quizDifficulties[Math.floor(Math.random() * quizDifficulties.length)];
//This line defines the URL for the API endpoint from which the quiz
// questions will be fetched.
  const API_URL = '/api/question-list/';

// Functionalities
/**
 * Start counting time in every single second.
 */

//This function, startCountdown(), is responsible for starting a countdown 
//timer for each quiz. It uses the setInterval function to update the timer 
//display on the page every second (1000 milliseconds).
function startCountdown() {
    let currentWidth = 100;

    return (intervalId = setInterval(() => {
        if (currentTime > 0) {
            currentWidth -= 100 / totalTime; // * get the percentage of total time and decrease it every interval
            if (currentTime <= 10) {
                countdownTimeBar.style.background = `linear-gradient(270deg,#ff8271,#ff523b)`;
            }
            countdownTimeBar.style.width = `${
                currentWidth ? currentWidth : 1
            }%`;
            currentTime--;
        } else {
            clearInterval(intervalId);
        }
    }, 1000));
}

/**
 * Return the final result of the user.
 * This function, getResult(), calculates and displays
 *  the user's final result at the end of the quiz. It compares the user's
 *  score with the pass mark and displays a message accordingly.
 */
function getResult() {
    const percentage = parseInt((passMark * quizAmount) / 100);
    if (currentTime > 0) {
        // ? time remain
        if (countCorrect >= percentage) {
            // * Win
            document.querySelector(".quiz-container").innerHTML = `
            <h2 class="result-heading">congratulation, you win!</h2>
            <p class="result-para">your score is: <span>${countCorrect}</span></p>
        `;
            document.querySelector(".result-para span").style.color = "#1DD881";
        } else {
            // ! Lost
            document.querySelector(".quiz-container").innerHTML = `
            <h2 class="result-heading">try again.</h2>
            <p class="result-para">your score is: <span>${countCorrect}</span></p>
        `;
            document.querySelector(".result-para span").style.color = "#ff523b";
        }
    } else {
        // ! times up
        if (countCorrect >= percentage) {
            // * Win but times up
            document.querySelector(".quiz-container").innerHTML = `
            <h2 class="result-heading">you passed but your times up!</h2>
            <p class="result-para">your score is: <span>${countCorrect}</span></p>
        `;
            document.querySelector(".result-para span").style.color = "#ff523b";
        } else {
            // ! Lost
            document.querySelector(".quiz-container").innerHTML = `
            <h2 class="result-heading">try again.</h2>
            <p class="result-para">your score is: <span>${countCorrect}</span></p>
        `;
            document.querySelector(".result-para span").style.color = "#ff523b";
        }
    }
}

/**
 * Update the results variables.
 */
function updateResult() {
    countIncorrect = answers.filter((answer, ind) => {
        return answer !== correctAnswers[ind];
    }).length;
    countCorrect = answers.filter((answer, ind) => {
        return answer === correctAnswers[ind];
    }).length;
}

/**
 * Render all the question into the corresponding placeholder.
 *
 * @param {Object} questions - All the questions as an array of object.
 * 
 * This function, renderQuestion(questions), takes an array of question 
 * objects as an argument and returns another function. This returned function 
 * is responsible for rendering each question and its options on the quiz interface. 
 * It iterates through the questions, displays them, and sets up event listeners
 *  for user interactions.
 */
function renderQuestion(questions) {
    let currentQuizIndex = 0;

    return function () {
        // Render the next question!
        quizQuestionEl.innerHTML =
            quizOptionListEl.innerHTML =
            quizControls.innerHTML =
                "";

        if (currentQuizIndex <= questions.length - 1) {
            const quiz = questions[currentQuizIndex];

            // Check if quiz.incorrect_answers is an array
            const options = Array.isArray(quiz.incorrect_answers)
                ? quiz.incorrect_answers.concat(quiz.correct_answer).sort(() => Math.random() - 0.5)
                : [quiz.correct_answer]; // Use only the correct answer if incorrect_answers is not an array

            quizNumberEl.innerHTML = `
                <h3>#${currentQuiz} <span>of ${questions.length}</span></h3>
            `;
            quizIncorrectSpan.innerText = countIncorrect;
            quizCorrectSpan.innerText = countCorrect;

            quizQuestionEl.innerText = quiz.question.replace(
                /&#(\d+);/gi,
                (match, charCode) => {
                    return String.fromCharCode(charCode);
                }
            );

            options.forEach((option, ind) => {
                const optionHeading = ["a", "b", "c", "d"];
                quizOptionListEl.innerHTML += `
                    <li>
                        <h3>${optionHeading[ind]}</h3>
                        <p>${option}</p>
                    </li>
                `;
                quizControls.innerHTML += `
                    <button data-answer=${JSON.stringify(
                        option
                    )} class="btn btn-option">${optionHeading[ind]}</button>
                `;
            });

            const optionButtons = document.querySelectorAll(".btn-option");
            optionButtons.forEach((optionButton) => {
                optionButton.addEventListener("click", (e) => {
                    [...optionButtons]
                        .filter((el) =>
                            el.classList.contains("btn-selected-option")
                        )
                        .forEach((el) =>
                            el.classList.remove("btn-selected-option")
                        );

                    answers.push(e.target.dataset.answer);
                    updateResult();
                    nextQuestion();
                });
            });

            currentQuiz++;
            ++currentQuizIndex;
        } else {
            // Quiz is completed!
            getResult();
        }
    };
}
/**
 * Request to the `opentdb.com` server to get all questions.
 * @return {string[]} - Return all the questions as an array.
 */

// This getQuestions() function sends a request to the API defined by 
// API_URL to fetch quiz questions. It uses the fetch API to make 
// the request and await for the response. If the API returns valid
//  questions, it logs the response and returns the questions as an array of 
//  objects. If there are no questions or an error occurs, it throws an error
//   message and returns an empty array.

javascript
async function getQuestions() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        console.log("API Response:", data); // Debugging: Log the API response

        if (Array.isArray(data) && data.length > 0) {
            return data;
        } else {
            throw "No questions were returned by the API.";
        }
    } catch (err) {
        console.error("API Error:", err); // Debugging: Log API errors
        return [defaultQuestion];
    }
}

// The init() function is the entry point of the application.
// It initializes the quiz by first fetching questions using the
//  getQuestions() function. Then, it sets up the countdown timer, 
//  updates the quiz topic displayed on the page, and calls renderQuestion
//  (questions) to start rendering the quiz questions. 
// If any error occurs during initialization, it displays an error message.
async function init() {
    try {
        const questions = await getQuestions();

        // insert all correct question into an array
        questions.forEach((question) => {
            correctAnswers.push(question.correct_answer);
        });

        startCountdown();

        quizTopicSpan.innerText = quizTopic;

        nextQuestion = renderQuestion(questions);
        nextQuestion();
    } catch (err) {
        document.querySelector(".quiz-section").innerHTML = `
            <h1 class="error-heading">check your internet connection.</h1>
        `;
        console.log(err);
    }
}

// * Initialize the app
init();
//Finally, these lines call the init()
// function to start the quiz application when the page loads.