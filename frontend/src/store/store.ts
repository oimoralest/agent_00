import { configureStore } from '@reduxjs/toolkit'
import projectReducer from './slice/project'
import agentReducer from './slice/agent'

export default configureStore({
  reducer: {
    project: projectReducer,
    agent: agentReducer,
  }
})
