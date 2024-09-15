const getAvailableTargets = (agent: any) => {
  console.log(agent);
  const targets = agent.nodes.filter((node: any) => node.input || node.inputs ? true : false);
  return targets;
}

export default getAvailableTargets;
