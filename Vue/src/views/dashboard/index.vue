<template>
  <div class="dashboard-container">
    <div class="dashboard-text">
      TryoutProject<br />
      Developers: Zefan Cai, Atith Gandhi, Jason Liu, Damian Rene, Raj Shah
      </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
