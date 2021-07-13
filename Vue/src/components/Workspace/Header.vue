<!--
Developers: Jason Liu
-->

<template>
  <div class="header">
    <div class="dropdown">
      <a id="menu" class="fas fa-chevron-circle-down btn" @click="toggleMenu" />
      <div
        :class="['menu', 'expandable', classMenu('menu')]"
        @mouseleave="showMenu['menu'] = false"
      >
        <a id="add-widget" class="menu-item" @click="toggleMenu">Add Widget</a>
        <div :class="['sub-menu', 'expandable', classMenu('add-widget')]">
          <div
            v-for="widget_type in widget_types"
            class="sub-menu-item"
            :key="widget_type"
            @click="addWidget(widget_type)"
          >
            {{ widget_type }}
          </div>
          <div v-show="widget_types.length == 0" class="sub-menu-item">
            All widgets added
          </div>
        </div>
        <a id="load-qa" class="menu-item" @click="toggleMenu">Load QA</a>
        <div :class="['sub-menu', 'expandable', classMenu('load-qa')]">
          <div
            v-for="qa in qas"
            class="sub-menu-item"
            :key="qa.id"
            @click="loadQA(qa.id)"
          >
            {{ qa.title }}
          </div>
          <div v-show="qas.length == 0" class="sub-menu-item">
            No loadable QAs
          </div>
        </div>
        <a id="create-qa" class="menu-item" @click="createQA">Create QA</a>
      </div>
    </div>
    <input v-model="workspace.title" />
    <a class="fas fa-minus btn" @click="minimize" />
    <a class="fas fa-times btn" @click="close" />
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    workspace_id: Number,
  },
  computed: {
    workspace() {
      return this.$store.getters.workspace(this.workspace_id);
    },
    widget_types() {
      let added_types = this.workspace.widgets.map((widget) => widget.type);
      return this.$store.state.widget_types.filter(
        (type) => !added_types.includes(type)
      );
    },
    qas() {
      return this.workspace.qas.filter(
        (qa) => qa.id !== this.workspace.qa_selected
      );
    },
  },
  data() {
    return {
      showMenu: {
        menu: false,
        "add-widget": false,
        "load-qa": false,
      },
    };
  },
  methods: {
    toggleMenu(event) {
      event.preventDefault();
      this.showMenu[event.target.id] = !this.showMenu[event.target.id];
    },
    classMenu(name) {
      return this.showMenu[name] ? "show-menu" : "";
    },
    addWidget(type) {
      this.$store.commit("addWidget", {
        workspace_id: this.workspace_id,
        type: type,
      });
    },
    loadQA(id) {
      this.workspace.qa_selected = id;
    },
    createQA() {
      this.$store.commit("createQA", this.workspace_id);
    },
    minimize() {},
    close() {
      this.$store.commit("deleteWorkspace", this.workspace_id);
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  margin: 0px;
  padding: 10px;
  font-size: 24px;
  border-bottom: 2px solid steelblue;
}

.fas {
  width: 30px;
  text-align: right;
}

.fa-chevron-circle-down {
  text-align: left;
}

.menu {
  display: flex;
  flex-direction: column;
  background-color: rgba(256, 256, 256, 0.98);
  border: 2px solid steelblue;
  border-radius: 4px;
  padding: 0px;
  position: absolute;
  z-index: 1;
}

.menu-item {
  font-size: 18px;
  cursor: pointer;
  padding: 6px;
  box-sizing: border-box;
}

.menu-item:hover {
  background-color: rgba(248, 248, 248, 0.98);
}

.sub-menu {
  background-color: rgba(241, 241, 241, 0.98);
  width: auto;
}

.sub-menu-item {
  font-size: 14px;
  cursor: pointer;
  padding: 6px;
  padding-top: 2px;
  padding-bottom: 2px;
  transition: background-color 0.3s;
  height: 20px;
}

.sub-menu-item:hover {
  background-color: rgba(234, 234, 234, 0.98);
}

.expandable {
  overflow: hidden;
  visibility: hidden;
  opacity: 0;
  max-height: 0;
  transition: opacity 0.2s, visibility 0s 0.2s linear;
}

.show-menu {
  visibility: visible;
  opacity: 1;
  max-height: 1000px;
  transition: opacity 0.2s, visibility 0s 0s linear;
}

input {
  width: auto;
  border: 0;
  font-weight: bold;
  outline: none;
  flex-grow: 1;
  text-overflow: ellipsis;
  padding: 0;
  padding-left: 10px;
}
</style>