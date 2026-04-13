import type { Meta, StoryObj } from '@storybook/react';
import { FinbroLogo } from './finbro-logo';

const meta: Meta<typeof FinbroLogo> = {
  title: 'Brand/FinbroLogo',
  component: FinbroLogo,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof FinbroLogo>;

export const Default: Story = {
    args: {
        className: 'text-white'
    }
};

export const Cobalt: Story = {
    args: {
        className: 'text-[#0047AB]'
    }
};
