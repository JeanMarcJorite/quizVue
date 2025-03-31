Quiz.vue
<script>

import Question from './Question.vue';


let question = {};
let verif = false;
let showInput = false;
let typeSelectionnée = 'simpleQuestion';
export default {
  props: {
    quiz: Object,
  },
  emits: ['removeQuiz', 'modifyQuiz'],
  data() {
    return {
      isEditing: false,
      isEditingQuestion: false,
      editedName: this.quiz.name,
      question,
      verif,
      showInput,
      typeSelectionnée,
      titleQuestion: '',
      newAnswer: '',
      newAnswers: ['', ''],
      reponseChoisi: null,

    };
  },
  methods: {
    handleRemoveQuiz() {
      this.$emit('removeQuiz', this.quiz.id);
    },
    handleModifyQuiz() {
      this.$emit('modifyQuiz', { id: this.quiz.id, name: this.editedName });
      this.isEditing = false;
    },

    afficherQuestion() {
      this.showInput = !this.showInput;
    },


    getQuestions() {
      this.isEditingQuestion = !this.isEditingQuestion;
      if (this.verif) {
        this.verif = false;
      } else {

        fetch('http://127.0.0.1:5000/quiz/api/v1/quiz/' + this.quiz.id)
          .then(response => response.json())
          .then(json => {
            this.verif = true;
            console.log(json.quiz);

            this.question = json.quiz;
          });
      }
    },
    removeQuestion(id) {
      console.log("id:", id);
      fetch('http://127.0.0.1:5000/quiz/api/v1/quiz/' + this.quiz.id + '/' + id, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
      })
        .then(response => response.json())
        .then(json => {
          this.question = this.question.filter(q => q.id !== id);
        });
    },
    handleEditQuiz() {
      this.isEditing = true;
    },
    cancelEditQuiz() {
      this.isEditing = false;
    },
    async modifyQuestionSimple({ id, title, reponse }) {
      try {


        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1/quiz/${this.quiz.id}/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title,
            questionnaire_id: this.quiz.id,
            reponse: reponse,
          }),
        });
        if (!response.ok) throw new Error("Échec de la requête");
        const json = await response.json();
        console.log("json:", json);
        this.question = this.question.map(q => (q.id === id ? json.question : q));
      } catch (e) {
        console.error("Erreur lors de la modification de la question :", e);
      }
    },


    async modifyQuestionMultiple({ id, title, proposition1, proposition2, bonne_reponse }) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/quiz/api/v1/quiz/${this.quiz.id}/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title,
            questionnaire_id: this.quiz.id,
            proposition1: proposition1,
            proposition2: proposition2,
            bonne_reponse: bonne_reponse,
          }),
        });

        if (!response.ok) throw new Error("Échec de la requête");
        const json = await response.json();
        this.question = this.question.map(q => (q.id === id ? json.question : q));
      } catch (e) {
        console.error("Erreur lors de la modification de la question multiple :", e);
      }
    },
    addQuestion() {
            let questionData;
            if (this.typeSelectionnée === 'simpleQuestion') {
                questionData = {

                    title: this.titleQuestion,
                    reponse: this.newAnswer,
                    questionType: this.typeSelectionnée
                };
            } else if (this.typeSelectionnée === 'multipleChoiceQuestion') {
                questionData = {
                    title: this.titleQuestion,
                    proposition1: this.newAnswers[0],
                    proposition2: this.newAnswers[1],
                    bonne_reponse: this.reponseChoisi,
                    questionType: this.typeSelectionnée
                };
            }
            fetch("http://127.0.0.1:5000/quiz/api/v1/quiz/" + this.quiz.id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questionData)
            })
                .then(response => response.json())
                .then(json => {
                    this.question.push(questionData);
                });
              this.showInput = false;
        },

  },

  components: {
    Question,
  },
};
</script>

<template>
  <div class="container">
    <div class="col-12" v-if="quiz">
      <div v-if="isEditing">
        <input v-model="editedName" type="text" class="form-control" placeholder="Modifier le nom du quiz" />
        <button @click="handleModifyQuiz" class="btn btn-success mt-2">Enregistrer</button>
        <button @click="cancelEditQuiz" class="btn btn-secondary mt-2" style="margin-left: 10px;">Annuler</button>
      </div>
      <div v-else>
        <h2 style="color: crimson;">{{ quiz.name }}</h2>
        <div v-if="!isEditingQuestion">
          <button class="btn btn-success mt-2" style="margin: 10px;" @click="getQuestions" id="show">Voir les
            questions</button>
        </div>
        <div v-if="isEditingQuestion">
          <button class="btn btn-success mt-2" style="margin: 10px;" @click="getQuestions" id="show">Cacher les
            questions</button>
        </div>
        <button @click="handleEditQuiz" class="btn btn-primary">Modifier</button>
        <button @click="handleRemoveQuiz" class="btn btn-danger" style="margin-left: 10px;">Supprimer</button>
      </div>
      <div v-if="verif">
        <button v-if="!showInput" @click="afficherQuestion" class="btn btn-secondary" style="margin: 10px;">Ajouter Une
          Question</button>
        <button v-else @click="afficherQuestion" class="btn btn-secondary" style="margin: 10px;">Annuler
          l'ajout</button>
        <div v-if="showInput">
          <input v-if="showInput" type="text" placeholder="Nouvelle question" v-model="titleQuestion" />
          <div>
            <select v-model="typeSelectionnée">
              <option>simpleQuestion</option>
              <option>multipleChoiceQuestion</option>
            </select>
            <div v-if="typeSelectionnée == 'simpleQuestion'">
              <input type="text" placeholder="Nouvelle reponse" v-model="newAnswer" />
            </div>
            <div v-if="typeSelectionnée == 'multipleChoiceQuestion'">
              <div v-for="(_, index) in newAnswers">
                <input type="text" placeholder="Nouvelle reponse" v-model="newAnswers[index]" />
                <input type="radio" v-model="reponseChoisi" :value="index + 1" />
              </div>
            </div>
            <div v-if="typeSelectionnée == 'simpleQuestion'">
            </div>
            <div v-if="typeSelectionnée == 'multipleChoiceQuestion'">
            </div>
          </div>
          <button @click="addQuestion" class="btn btn-success">Valider</button>

        </div>
      </div>

    </div>
    <div v-if="verif">
      <div v-for="q of question">
        <Question :question="q" @removeQuestion="removeQuestion" @modifyQuestionSimple="modifyQuestionSimple"
          @modifyQuestionMultiple="modifyQuestionMultiple">
        </Question>
      </div>
    </div>
  </div>
</template>