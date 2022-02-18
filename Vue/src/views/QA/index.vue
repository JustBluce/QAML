<!--
Developers: Jason Liu, Cai Zefan, and Damian Rene
-->

<template>
  <div>
    <Taskbar title="QA Interface" :qa="true" />
    <v-container fluid class="workspaces-container">
      <div
        v-if="workspace_stack.length == 0"
        style="height: 100%; opacity: 0.7"
      >
        <v-row dense align="end" justify="center" style="height: 50%">
          <v-icon size="400">mdi-tab-plus</v-icon>
        </v-row>
        <v-row dense align="start" justify="center" style="height: 50%">
          <p class="text-h4 text--secondary">
            Click "<span style="color: var(--v-green-base); font-weight: bold"
              >+</span
            >" to create a workspace
          </p>
        </v-row>
      </div>
      <transition-group
        tag="div"
        style="height: 150%; width: 150%"
        type="transition"
        name="workspaces"
      >
        <Workspace
          v-for="workspace_id in workspace_stack"
          :key="workspace_id"
          :id="workspace_id"
        />
      </transition-group>
    </v-container>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import firebase from "firebase";
import Taskbar from "@/components/Taskbar";
import Workspace from "@/components/Workspace";

export default {
  name: "QA",
  components: {
    Taskbar,
    Workspace,
    draggable,
  },
  data() {
    return {
      drag: false,
    };
  },
  computed: {
    workspace_stack() {
      return this.$store.state.workspace_stack;
    },
  },
  methods: {
    updateFirebaseVuex() {
      // Sends state to firestore
      
       if(firebase.auth().currentUser.isAnonymous == false){
      console.log("Updating Workspace On the Backend");
      const db = firebase.firestore();
      const docs = db
        .collection("users")
        .doc(this.user_id)
        .collection("workspace")
        .doc("workspaceState");
      //console.log(this.$store.state.workspaces)
      console.log(this.$store.state.workspacew_index)
      docs.set(
          {
            workspaces: this.$store.state.workspaces,
                workspace_selected: this.$store.state.workspace_selected,
               
           
            //widget_types: this.$store.state.widget_types,
            //game_mode: this.$store.state.game_mode,

            //recommended: this.$store.state.recommended,
            //timestamp: firebase.firestore.Timestamp.now(),
          },
          { merge: true }
        )
        .catch((err) => {
          alert("DOCUMENTS Oops.(QA.index) " + err.message);
        });
       }else{
         console.log("GUEST ACCOUNT: Not sending updates to the backend")
       }
    },
  },
  created() {
 
     this.user_id = firebase.auth().currentUser.uid;
  },
  mounted() {
    const db = firebase.firestore();
    if(firebase.auth().currentUser.uid != null){
      const docs = db.collection("users").doc(this.user_id).collection("workspace");
      docs
        .where("workspaces", "!=", null)
        .get()
        .then((snapshot) => {
          snapshot.docs.forEach((doc) => {
            if (doc.exists) {
              console.log("Found old Workspace... Restoring");
              console.log(doc.data().workspaces);
              
              //console.log(doc.data().workspaces[0])
               this.$store.commit("uploadWorkspaces", doc.data().workspaces,doc.data().workspace_selected );
            }
          });
        });

      this.timer = setInterval(() => {
        this.updateFirebaseVuex();
      }, 10000);
    }else{
      console.log("GUEST ACCOUNT: Not sending updates to the backend")
    } 
  },
  beforeDestroy() {
    clearInterval(this.timer);
    this.updateFirebaseVuex();
  },
};
</script>

<style>
.workspaces-container {
  position: relative;
  overflow: hidden;
  height: calc(100vh - 100px);
  padding: 8px;
}

.workspaces-enter-active,
.workspaces-leave-active {
  position: relative;
  height: 100%;
  z-index: 1000;
}

.workspaces-enter {
  transform: translate(0, -100vh);
}

.workspaces-enter-active {
  transition: all 0.3s ease;
}

.workspaces-leave-to {
  transform: translate(0, -200vh);
}

.workspaces-leave-active {
  transition: all 0.5s ease;
}

.ghost {
  opacity: 0.3;
}
</style>