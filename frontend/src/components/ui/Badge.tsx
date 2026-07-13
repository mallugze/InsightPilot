import React from 'react';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  className?: string;
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  className = '',
  children,
  ...props
}) => {
  return (
    <span
      className={`${className}`}
      {...props}
    >
      {children}
    </span>
  );
};
