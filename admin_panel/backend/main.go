package main

import (
	"database/sql"
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	_ "github.com/mattn/go-sqlite3"
)

type TemplateRegistry struct {
	templates *template.Template
}

func (t *TemplateRegistry) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

var globalNationName string
var globalTableName string

func main() {
	app := echo.New()
	wd, err := os.Getwd()
	if err != nil {
		fmt.Println("Error getting working directory:", err)
		return
	}

	app.Renderer = &TemplateRegistry{
		templates: template.Must(template.ParseGlob(wd + "/admin_panel/frontend/*.html")),
	}

	app.GET("/", func(c echo.Context) error {
		return c.Render(200, "index.html", nil)
	})

	app.GET("/modify", handleData)
	app.GET("/api/modify", sendData)
	app.POST("/update", update)

	app.Start(":8000")
}

func handleData(c echo.Context) error {
	nationName := c.QueryParam("nation_name")
	sqlTable := c.QueryParam("table")

	globalNationName = nationName
	globalTableName = sqlTable

	data := map[string]interface{}{
		"nation_name": nationName,
		"table":       sqlTable,
	}

	return c.Render(200, "modify.html", data)
}

func sendData(c echo.Context) error {
	nationName := c.QueryParam("nation_name")
	sqlTable := c.QueryParam("table")
	wd, err := os.Getwd()
	if err != nil {
		fmt.Println("Error getting working directory:", err)
		panic(err)
	}

	db, err := sql.Open("sqlite3", wd+"/player_info.db")
	if err != nil {
		fmt.Println("Database connection error:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Database connection failed"})
	}
	defer db.Close()

	query := fmt.Sprintf("SELECT * FROM %s WHERE name = ?", sqlTable)
	fmt.Println("Executing query:", query)

	rows, err := db.Query(query, nationName)
	if err != nil {
		fmt.Println("Query execution error:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Query execution failed"})
	}
	defer rows.Close()

	var rowsData []map[string]interface{}
	for rows.Next() {
		columns, err := rows.Columns()
		if err != nil {
			return err
		}

		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))
		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			return err
		}

		rowMap := make(map[string]interface{})
		for i, colName := range columns {
			var value interface{}
			if b, ok := values[i].([]byte); ok {
				value = string(b)
			} else {
				value = values[i]
			}
			rowMap[colName] = value
		}

		rowsData = append(rowsData, rowMap)
	}

	return c.JSON(http.StatusOK, rowsData)
}

type Reponse struct {
	Message string `json:"message"`
}

func update(c echo.Context) error {
	columnToModify := c.FormValue("columnToModify")
	operation := c.FormValue("operation")
	amount := c.FormValue("amount")

	db, err := sql.Open("sqlite3", "/home/void/python_projects/pw_custom/player_info.db")
	if err != nil {
		fmt.Println("Database connection error:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Database connection failed"})
	}
	defer db.Close()

	if operation == "add" {
		operation = "+"
	} else {
		operation = "-"
	}

	if columnToModify == "name" {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": "Name column cannot be modified"})
	}

	query := fmt.Sprintf("UPDATE %s SET %s = %s %s ? WHERE name = ?", globalTableName, columnToModify, columnToModify, operation)
	fmt.Println("Executing query:", query)

	_, err = db.Exec(query, amount, globalNationName)
	if err != nil {
		fmt.Println("Query execution error:", err)
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Query execution failed"})
	}

	response := &Reponse{
		Message: "Data updated successfully",
	}

	// Process the form data
	return c.JSON(200, response)
}
