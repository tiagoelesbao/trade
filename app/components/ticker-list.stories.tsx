import type { Meta, StoryObj } from '@storybook/react';
import { TickerList } from './ticker-list';

const meta: Meta<typeof TickerList> = {
  title: 'Components/TickerList',
  component: TickerList,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof TickerList>;

export const Default: Story = {};
