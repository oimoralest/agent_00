import { Modal, ModalContent } from '@nextui-org/react';

import Agent from './agent';
import Timer from './timer';
import LLM from './node/llm'
import InputNode from './node/input';

const Editable = ({ isOpen, onOpenChange, type }) => {
  const contentMapper = {
    'agent': <Agent />,
    'timer': <Timer />,
    'llm': <LLM />,
    'input': <InputNode />,
  }

  return (
    <Modal isOpen={isOpen} onOpenChange={onOpenChange}>
      <ModalContent>
        {contentMapper[type]}
      </ModalContent>
    </Modal>
  )
}

export default Editable;
