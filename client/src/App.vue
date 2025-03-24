<script>
import Quiz from './components/Quiz.vue';

export default {
  name: 'QuizApp',
  components: {
    Quiz,
  },
  data() {
    return {
      data: [],
      newQuizName: '',
      editQuiz: false,
    };
  },
  mounted() {
    fetch('http://127.0.0.1:5000/quiz/api/v1/quiz/')
      .then(response => response.json())
      .then(json => {
        console.log("rep API:", json);
        this.data = json.quiz || [];
      })
      .catch(console.error);
  },
  methods: {
    addQuiz: async function (newQuizName) {
      if (newQuizName) {
        fetch('http://127.0.0.1:5000/quiz/api/v1/quiz/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newQuizName,
          })
        })
          .then(response => response.json())
          .then(json => {
            this.data.push(json.quiz);
          });
      }
    },
    removeQuiz: async function (id) {
      fetch('http://127.0.0.1:5000/quiz/api/v1/quiz/' + id, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
      })
        .then(response => response.json())
        .then(json => {
          this.data = this.data.filter(quiz => quiz.id !== id);
        });
    },

    modifyQuiz: async function ({ id, name }) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1/quiz/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name }),
        });

        if (!response.ok) throw new Error("Échec de la requête");

        const rep = await response.json();
        if (rep.quiz) {
          this.data = this.data.map(quiz => {
            if (quiz.id === id) {
              return rep.quiz;
            }
            return quiz;
          });
        }
      } catch (error) {
        console.error("Échec de la modification:", error);
      }
    },
    editListQuiz: function () {
      this.editQuiz = !this.editQuiz;
      if (this.editQuiz) {
        document.getElementById("edit").innerHTML = "Terminer l'édition";
        document.getElementById("edit").className = "btn btn-success mt-5";
      }else{
        document.getElementById("edit").innerHTML = "Ajouter Un Quiz";
        document.getElementById("edit").className = "btn btn-warning mt-5";
        this.addQuiz(this.newQuizName);
        this.newQuizName = '';
      }
    }
  }
};
</script>

<template>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
    integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
  <div>
    <h2>Mes Quiz</h2>
    <Quiz v-for="q in data" :key="q.id" :quiz="q" @removeQuiz="removeQuiz" @modifyQuiz="modifyQuiz"></Quiz>
    <span class="input-group-btn" v-if="editQuiz">
      <input v-model="newQuizName" type="text" class="form-control" placeholder="Nom du quiz" />
    </span>
    <button @click="editListQuiz" class="btn btn-warning mt-5" type="button" id="edit">
        Ajouter Un Quiz
      </button> 
  </div>
</template>