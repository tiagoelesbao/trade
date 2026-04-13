import type { Meta, StoryObj } from '@storybook/react';
import { PerformanceChart } from './performance-chart';

const meta: Meta<typeof PerformanceChart> = {
  title: 'Components/PerformanceChart',
  component: PerformanceChart,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof PerformanceChart>;

export const Default: Story = {};
