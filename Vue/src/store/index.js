/**
 * Developers: Jason Liu, Damian Rene
 */

import Vue from 'vue';
import Vuex from 'vuex';
import * as getters from './getters';
import { defaultWorkspace, initial_workspaces, widget_types } from './workspace';
import app from './modules/app';
import settings from './modules/settings';
import VueGoogleCharts from 'vue-google-charts';
import firebase from 'firebase';
import { vuexfireMutations, firestoreAction } from 'vuexfire';

Vue.use(VueGoogleCharts);
Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        workspaces: initial_workspaces,
        workspace_stack: initial_workspaces.map((workspace) => workspace.id),
        workspace_index: initial_workspaces.length,
        workspace_selected: initial_workspaces[0].tab_id,
        widget_types: widget_types,
        widget_usages: widget_types.reduce((ac, a) => ({ ...ac, [a]: 0 }), {}),
        game_mode: false,
        genreChartData: [ [ 'Genre', 'Count' ], [ 'None', 1 ] ],
        recommended: [ 'Baltimore', 'Washington, D.C.', 'Cleveland' ]
    },

    modules: {
        app,
        settings
    },
    mutations: {
        ...vuexfireMutations,
        createWorkspace(state, title) {
            let newWorkspace = defaultWorkspace(state.workspace_index);
            if (title) {
                newWorkspace.title = title;
                state.recommended = state.recommended.filter((rec) => rec !== title);
            }
            state.workspaces.push(newWorkspace);
            state.workspace_index++;
            this.commit('updateTabs');
            this.commit('selectWorkspace', newWorkspace.id);
        },
        addWorkspace(state, workspace_id) {
            getters.workspace(state)(workspace_id).tab = true;
            this.commit('updateTabs');
            this.commit('selectWorkspace', workspace_id);
        },
        closeWorkspace(state, workspace_id) {
            this.commit('minimizeWorkspace', workspace_id);
            getters.workspace(state)(workspace_id).tab = false;
        },
        selectWorkspace(state, workspace_id) {
            let last_workspace_id = state.workspace_stack.slice(-1)[0];
            state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
            state.workspace_stack.push(workspace_id);
            state.workspace_selected = getters.workspace(state)(workspace_id).tab_id;
            if (last_workspace_id != null && last_workspace_id != workspace_id) {
                widget_types.forEach((type) =>
                    this.commit('toggleWidget', { workspace_id: last_workspace_id, type, toggle: 0, select: true })
                );
                widget_types.forEach((type) =>
                    this.commit('toggleWidget', { workspace_id, type, toggle: 1, select: true })
                );
            }
        },
        minimizeWorkspace(state, workspace_id) {
            let toggle = workspace_id === state.workspace_stack.slice(-1)[0];
            if (toggle) {
                widget_types.forEach((type) =>
                    this.commit('toggleWidget', { workspace_id, type, toggle: 0, select: true })
                );
            }
            state.workspace_stack = state.workspace_stack.filter((id) => id !== workspace_id);
            if (state.workspace_stack.length > 0) {
                let newWorkspace_id = state.workspace_stack.slice(-1)[0];
                state.workspace_selected = getters.workspace(state)(newWorkspace_id).tab_id;
                if (toggle) {
                    widget_types.forEach((type) =>
                        this.commit('toggleWidget', { workspace_id: newWorkspace_id, type, toggle: 1, select: true })
                    );
                }
            } else {
                state.workspace_selected = 0;
            }
        },
        resetWorkspace(state, workspace_id) {
            initial_workspaces;
            let workspace = getters.workspace(state)(workspace_id);
            let resetWorkspace = defaultWorkspace(0);
            workspace.qa = resetWorkspace.qa;
            workspace.widgets = resetWorkspace.widgets;
            workspace.results = resetWorkspace.results;
        },
        deleteWorkspace(state, workspace_id) {
            this.commit('closeWorkspace', workspace_id);
            state.workspaces = state.workspaces.filter((workspace) => workspace.id !== workspace_id);
            state.workspace_index--;
            this.commit('updateTabs');
        },
        updateTabs(state) {
            state.workspace_selected =
                state.workspaces.findIndex((workspace) => workspace.tab_id === state.workspace_selected) + 1;
            state.workspaces = state.workspaces.map((workspace, i) => Object.assign(workspace, { tab_id: i + 1 }));
        },
        toggleWidget(state, { workspace_id, type, toggle, select = false }) {
            let workspace = getters.workspace(state)(workspace_id);
            let widget = workspace.widgets.find((widget) => widget.type === type);
            if ((!select && widget.show !== toggle) || (select && widget.show)) {
                if (!select) {
                    widget.show = toggle;
                }
                switch (toggle) {
                    case 0:
                        state.widget_usages[type] += Math.floor(
                            (Date.now() - workspace.widget_timestamps[type]) / 1000
                        );
                    case 1:
                        workspace.widget_timestamps[type] = Date.now();
                }
            }
        },
        addResult(state, { workspace_id, result }) {
            let workspace = getters.workspace(state)(workspace_id);
            workspace.results.dialog = true;
            workspace.results.content.push(result);
        },
        closeResults(state, workspace_id) {
            let workspace = getters.workspace(state)(workspace_id);
            workspace.results.dialog = false;
            workspace.results.content = [];
        },
        loadFirebaseVuex(state) {
            const db = firebase.firestore();
            const user_id = firebase.auth().currentUser.uid;
            const override = false; // this is very scuffed if our Vuex json structure changes
            if (firebase.auth().currentUser.uid != null && !override) {
                const docs = db.collection('users').doc(user_id).collection('workspace');
                docs.where('workspaces', '!=', null).get().then((snapshot) => {
                    snapshot.docs.forEach((doc) => {
                        if (doc.exists) {
                            console.log('Found old Workspace... Restoring');
                            console.log(doc.data().workspaces);

                            //console.log(doc.data().workspaces[0])
                            state.workspaces = doc.data().workspaces;
                            state.workspace_stack = doc.data().workspace_stack;
                            state.workspace_index = doc.data().workspace_index;
                            state.workspace_selected = doc.data().workspace_selected;
                            this.commit('updateTabs');
                        }
                    });
                });
            } else {
                console.log('GUEST ACCOUNT: Not sending updates to the backend');
            }
        },
        updateFirebaseVuex(state) {
            if (firebase.auth().currentUser.isAnonymous == false) {
                console.log('Updating Workspace On the Backend');
                const db = firebase.firestore();
                const user_id = firebase.auth().currentUser.uid;
                const docs = db.collection('users').doc(user_id).collection('workspace').doc('workspaceState');
                docs
                    .set(
                        {
                            workspaces: state.workspaces,
                            workspace_stack: state.workspace_stack,
                            workspace_index: state.workspace_index,
                            workspace_selected: state.workspace_selected

                            //widget_types: this.$store.state.widget_types,
                            //game_mode: this.$store.state.game_mode,

                            //recommended: this.$store.state.recommended,
                            //timestamp: firebase.firestore.Timestamp.now(),
                        },
                        { merge: true }
                    )
                    .catch((err) => {
                        alert('DOCUMENTS Oops.(QA.index) ' + err.message);
                    });
            } else {
                console.log('GUEST ACCOUNT: Not sending updates to the backend');
            }
        }
    },
    getters: {
        //isLoggedIn: (state) => state.user.loggedIn,
        //userData: (state) => state.user.data,
        //verified: (state) => state.user.verified,

        sidebar: (state) => state.app.sidebar,
        device: (state) => state.app.device,
        //token: (state) => state.user.token,
        //avatar: (state) => state.user.avatar,
        //name: (state) => state.user.name,
        workspaces: (state) => {
            return state.workspaces;
        },
        ...getters
    },
    actions: {
        /* fetchUser({ commit }, user) {
			commit('SET_LOGGED_IN', user !== null);
			if (user) {
				commit('SET_USER', {
					displayName: user.displayName,
					email: user.email
				}),
				commit('SET_VERIFIED', {
					verified: user.emailVerified, 
				});
			} else {
				commit('SET_USER', null);
			}
		} */
    }
});

export default store;
