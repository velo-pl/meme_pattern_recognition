import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error: error };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error("Uncaught error in component:", error, errorInfo);
    this.setState({ errorInfo: errorInfo });
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div style={{ border: '1px solid red', padding: '10px', margin: '10px' }}>
          <h4>Something went wrong with this section.</h4>
          {this.props.sectionName && <p>Section: {this.props.sectionName}</p>}
          {this.state.error && <p>Error: {this.state.error.toString()}</p>}
          {this.state.errorInfo && (
            <details style={{ whiteSpace: 'pre-wrap' }}>
              {this.state.errorInfo.componentStack}
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

