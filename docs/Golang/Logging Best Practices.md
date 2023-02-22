# Logging Best Practices

### Logging level

There are typically 5 main log levels:

1.  **DEBUG**: for in-depth information that can help troubleshoot and resolve issues.
2.  **INFO**: for general information about the state of the application, such as user actions, system events, and other high-level details.
3.  **WARNING**: for potential issues that may need attention. This could include information about system failures, performance issues, or other events that don’t cause the application to fail but should still be monitored.
4.  **ERROR**: for information about actual failures or errors that occur within the application. This should include information about exceptions, stack traces, and other diagnostic information that can help pinpoint the cause of the issue.
5.  **FATAL**: for critical errors that cause the application to stop functioning.

### Structured

It allows developers to quickly and easily filter log messages to focus on the most important information. [See](https://betterprogramming.pub/why-you-should-use-structured-logging-format-47a388711316)

### Context

When it comes to logging, it’s not only about tracking the data you want to, context also plays an important role. For example, including:

- **Timestamp:** With a timestamp included with the log message, it’s easier to understand when an event occurred and can be helpful in troubleshooting issues related to time.
- **Service information:** Including the name of the service (e.g. order-service-0) or component (e.g. RetrieveOrderBusiness) that generated the log message can help understand the context of the event and can be helpful in troubleshooting issues related to specific services.
- **User information:** Who took the action, their state (e.g. banned or having too much money), etc.
- **Request information:** Request ID, the device/ browser used to make the request, client version, etc

It’s important to log with context, but also to log only what’s necessary.

### Rotation

Log rotation is the process of regularly moving or archiving old log files to prevent them from growing too large and to ensure that important information is not lost. Here some techniques to rotate:

1.  **Compressing**: To save on storage space, log files that are no longer needed can be compressed.
2.  **Archiving**: For long-term storage, old log files can be moved to a different location such as a separate disk or a remote server.
3.  **Deleting**: To clear up space, log files that are no longer needed can be deleted.
4.  **Truncating**: To keep the current logs, but remove the old log entries that are not needed.

Reference: https://medium.com/@func25/logging-best-practices-proven-techniques-for-services-b772eaedbe3f