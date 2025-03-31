// Question.vue
<script>

export default {
  props: {
    question: Object,
  },
  emits: ['modifyQuestionSimple', 'modifyQuestionMultiple', 'removeQuestion', 'addQuestionSimple', 'addQuestionMultiple'],
  data() {
    return {
       editQuestion: false,
    };
  },
  methods: {
        removeQuestion() {
          this.$emit('removeQuestion',  this.question.id );
        },
        handleModifyQuestion() {
  if (this.editQuestion) {
    if (this.question.questionType === 'simpleQuestion') {
      this.$emit('modifyQuestionSimple', {
        id: this.question.id,
        title: this.question.title,
        reponse: this.question.reponse,
      });
    } else {
      this.$emit('modifyQuestionMultiple', {
        id: this.question.id,
        title: this.question.title,
        proposition1: this.question.proposition1,
        proposition2: this.question.proposition2,
        bonne_reponse: this.question.bonne_reponse,
      });
    }
  }
  this.editQuestion = !this.editQuestion;
}
    }

}
</script>

<template>
    <div class="row">
        <div v-if="!editQuestion">
            <h3>{{ question.title }}</h3>
            <div v-if="question.questionType === 'simpleQuestion'">
                <p>{{ question.reponse }}</p>
            </div>
            <div v-if="question.questionType === 'multipleChoiceQuestion'">
                <p>{{ question.proposition1 }}</p>
                <p>{{ question.proposition2 }}</p>
                <p> Bonne réponse : {{ question.bonne_reponse }}</p>
            </div>

        </div>
        <div v-else>
            <input v-model="question.title" type="text" class="form-control" placeholder="Question">
            <div v-if="question.questionType === 'simpleQuestion'">
                <input v-model="question.reponse" type="text" class="form-control" placeholder="Réponse">
            </div>
            <div v-if="question.questionType === 'multipleChoiceQuestion'">
                <input v-model="question.proposition1" type="text" class="form-control" placeholder="Proposition 1">
                <input v-model="question.proposition2" type="text" class="form-control" placeholder="Proposition 2">
                <input v-model="question.bonne_reponse" type="text" class="form-control" placeholder="Bonne réponse">
            </div>
        </div>
    </div>
    <button @click="handleModifyQuestion"  class="btn btn-primary">Modifier</button>
    <button style="margin-left: 10px;"  @click="removeQuestion" class="btn btn-danger">Supprimer</button>
</template>