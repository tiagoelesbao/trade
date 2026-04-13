import type { Meta, StoryObj } from '@storybook/react'
import { AgentWarRoom } from './agent-war-room'

const meta: Meta<typeof AgentWarRoom> = {
  title: 'Components/AgentWarRoom',
  component: AgentWarRoom,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof AgentWarRoom>

export const Default: Story = {
  render: () => (
    <div className="w-[450px] bg-black p-6">
      <AgentWarRoom />
    </div>
  ),
}
