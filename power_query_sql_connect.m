// Replace the path below with full path to fd_data.db
let
    Source = Sql.Database("localhost", "unused-placeholder"), // Not used for SQLite; use UI
    // In Power BI Desktop: use "Get Data -> More -> SQLite database" and browse to fd_data.db
    // After connecting, select the 'validated_users', 'fd_bookings', and 'ai_summary' tables
    // This M block is for reference/instructions only.
    Note = "In Power BI Desktop use 'Get Data -> SQLite database' and select the file fd_data.db"
in
    Note
