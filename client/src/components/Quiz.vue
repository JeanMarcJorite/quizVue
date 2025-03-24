<script>
export default {
  props: {
    quiz: Object,
  },
  emits: ['removeQuiz', 'modifyQuiz'],
  data() {
    return {
      isEditing: false,
      editedName: this.quiz.name, 
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
    handleEditQuiz() {
      this.isEditing = true; 
    },
    cancelEditQuiz() {
      this.isEditing = false; 
    },
  },
};
</script>

<template>
  <div class="container">
    <div class="col-12" v-if="quiz">
      <div v-if="isEditing">
        <input
          v-model="editedName"
          type="text"
          class="form-control" 
          placeholder="Modifier le nom du quiz"
          
        />
        <button @click="handleModifyQuiz" class="btn btn-success mt-2">Enregistrer</button>
        <button @click="cancelEditQuiz" class="btn btn-secondary mt-2" style="margin-left: 10px;">Annuler</button>
      </div>
      <div v-else>
        <h2 style="color: crimson;">{{ quiz.name }}</h2>
        <button @click="handleEditQuiz" class="btn btn-primary">Modifier</button>
        <button @click="handleRemoveQuiz" class="btn btn-danger" style="margin-left: 10px;">Supprimer</button>
      </div>
    </div>
  </div>
</template>