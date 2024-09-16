// Libraries
import React from 'react'
import ReactDOM from 'react-dom/client'
import { NextUIProvider } from '@nextui-org/react';
import { Provider } from 'react-redux';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

// Styles
import './index.css'

// Routes
import Home from './route/home';
import Project from './route/project.tsx';
import Agent from './route/agent';

// Redux
import store from './store/store.ts';
import { fetchAgent } from './store/slice/agent.ts';
import { fetchProject } from './store/slice/project.ts';
import Background from './component/editable/background.tsx';

// Router
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    // TODO: Add auth validation
    path: "project/:projectId",
    element: <Project />,
    loader: async ({ params }) => {
      store.dispatch(fetchProject(params.projectId as string));
      return null;
    }
  },
  {
    // TODO: Add auth validation
    path: "agent/:agentId",
    element: <Agent />,
    loader: async ({ params }) => {
      store.dispatch(fetchAgent(params.agentId as string));
      return null;
    }
  },
]);


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Provider store={store}>
      <NextUIProvider>
        <Background />
        <RouterProvider router={router} />
      </NextUIProvider>
    </Provider>
  </React.StrictMode>,
)
