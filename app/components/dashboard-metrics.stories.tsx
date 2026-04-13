import type { Meta, StoryObj } from '@storybook/react';
import { DashboardMetrics } from './dashboard-metrics';

const meta: Meta<typeof DashboardMetrics> = {
  title: 'Components/DashboardMetrics',
  component: DashboardMetrics,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof DashboardMetrics>;

export const Default: Story = {};
