export default {
  testEnvironment: "jest-environment-jsdom",
  setupFilesAfterEnv: ["@testing-library/jest-dom"],
  transform: {
    "^.+\\.jsx?$": "babel-jest" // Transform JS and JSX files using babel-jest
  },
  moduleNameMapper: {
    // Handle CSS imports (if you have them in your components)
    "\\.(css|less|scss|sass)$": "identity-obj-proxy",
    // Handle image imports
    "\\.(gif|ttf|eot|svg|png)$": "<rootDir>/__mocks__/fileMock.js"
  },
  // Indicates whether each individual test should be reported during the run
  verbose: true,
  // Automatically clear mock calls and instances between every test
  clearMocks: true,
};

