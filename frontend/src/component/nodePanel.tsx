import { Button, Tooltip } from "@nextui-org/react"

const HEIGHT = "24"
const WIDTH = "24"

const NodePanel = ({ setOpenEditable, setNodeType }) => {
  // TODO: Use enum for node types
  return (
    <div className="flex flex-wrap gap-2">
      <Tooltip
        showArrow={true}
        content="Input node"
        placement="top"
      >
        <Button
          isIconOnly={true}
          onPress={() => {
            setOpenEditable(true);
            setNodeType("input");
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-braces"><path stroke="none" d="M0 0h24v24H0z" fill="none" /><path d="M7 4a2 2 0 0 0 -2 2v3a2 3 0 0 1 -2 3a2 3 0 0 1 2 3v3a2 2 0 0 0 2 2" /><path d="M17 4a2 2 0 0 1 2 2v3a2 3 0 0 0 2 3a2 3 0 0 0 -2 3v3a2 2 0 0 1 -2 2" /></svg>
        </Button>
      </Tooltip>
      <Tooltip
        showArrow={true}
        content="LLM node"
        placement="top"
      >
        <Button
          isIconOnly={true}
          onPress={() => {
            setOpenEditable(true);
            setNodeType("llm");
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="m19 1l-1.26 2.75L15 5l2.74 1.26L19 9l1.25-2.74L23 5l-2.75-1.25M9 4L6.5 9.5L1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5M19 15l-1.26 2.74L15 19l2.74 1.25L19 23l1.25-2.75L23 19l-2.75-1.26" /></svg>
        </Button>
      </Tooltip>
      <Tooltip
        showArrow={true}
        content="Time node"
        placement="top"
      >
        <Button
          isIconOnly={true}
          onPress={() => {
            setOpenEditable(true);
            setNodeType("timer");
          }}
        >
          <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
            <path fillRule="evenodd" d="M5.5 3a1 1 0 0 0 0 2H7v2.333a3 3 0 0 0 .556 1.74l1.57 2.814A1.1 1.1 0 0 0 9.2 12a.998.998 0 0 0-.073.113l-1.57 2.814A3 3 0 0 0 7 16.667V19H5.5a1 1 0 1 0 0 2h13a1 1 0 1 0 0-2H17v-2.333a3 3 0 0 0-.56-1.745l-1.616-2.82a1 1 0 0 0-.067-.102 1 1 0 0 0 .067-.103l1.616-2.819A3 3 0 0 0 17 7.333V5h1.5a1 1 0 1 0 0-2h-13Z" clipRule="evenodd" />
          </svg>

        </Button>
      </Tooltip>

    </div>
  )
}

export default NodePanel;
