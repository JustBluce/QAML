import Vue from 'vue';
import Vuex from 'vuex';
import { initial_widgets, widget_types, widgetTemplate } from './widgets';
import app from './modules/app';
import settings from './modules/settings';
import user from './modules/user';

Vue.use(Vuex);

const store = new Vuex.Store({
	state: {
		modal: {
			opened: false,
			difficulty: 'Easy',
			question_saved: false
		},
		widgets: initial_widgets,
		widget_types: widget_types,
		widget_index: initial_widgets.length,
		qa_index: initial_widgets.filter((widget) => widget.type === 'QA').length
	},
	modules: {
		app,
		settings,
		user
	},
	mutations: {
		addWidget(state, type) {
			type === 'QA' && state.qa_index++;

			state.widgets.push(widgetTemplate(state, type));
			state.widget_index++;
		},
		deleteWidget(state, id) {
			state.widgets = state.widgets.filter((widget) => widget.id !== id);
		},
		toggleWidget(state, id) {
			state.widgets = state.widgets.map(
				(widget) => (widget.id === id ? { ...widget, expanded: !widget.expanded } : widget)
			);
		},
		updateWidget(state, payload) {
			state.widgets = state.widgets.map(
				(widget) => (widget.id === payload.id ? Object.assign(widget, payload) : widget)
			);
		}
	},
	getters: {
		sidebar: (state) => state.app.sidebar,
		device: (state) => state.app.device,
		token: (state) => state.user.token,
		avatar: (state) => state.user.avatar,
		name: (state) => state.user.name,
		widget: (state) => (id) => state.widgets.filter((widget) => widget.id === id)[0],
		widget_template: (state) => (type) => widgetTemplate(state, type)
	}
});

export default store;
