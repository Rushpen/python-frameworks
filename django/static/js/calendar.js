document.addEventListener("DOMContentLoaded", () => {
  const daysContainer = document.querySelector(".days");
  const months = document.querySelectorAll(".months li a");
  const yearElement = document.querySelector(".year");
  const taskList = document.querySelector(".noteList");
  const monthNameElement = document.querySelector(".month-name");
  const dayInfoElement = document.querySelector(".day-info");
  const prevYearButton = document.getElementById("prevYear");
  const nextYearButton = document.getElementById("nextYear");

  let selectedDay = null;

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function getDaysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
  }

  function updateDays(month, year) {
    const daysInMonth = getDaysInMonth(month, year);
    daysContainer.innerHTML = "";

    for (let i = 1; i <= daysInMonth; i++) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#";
      a.textContent = i;
      a.dataset.value = i;

      const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        if (tasksByDate[formattedDate]) {
            a.classList.add("task-day");
        }

      li.appendChild(a);
      daysContainer.appendChild(li);
    }

    const days = document.querySelectorAll(".days li a");
    days.forEach((day) => {
      day.addEventListener("click", () => {
        days.forEach((d) => d.classList.remove("selected"));
        day.classList.add("selected");

        selectedDay = parseInt(day.dataset.value);
        const date = new Date(year, month - 1, selectedDay);
        const dayOfWeek = dayNames[date.getDay()];
        const formattedDate = `${year}-${String(month).padStart(2, '0')}-${String(selectedDay).padStart(2, '0')}`;

        dayInfoElement.textContent = `${dayOfWeek}, ${selectedDay}`;
        updateTaskList(formattedDate);
      });
    });

    if (selectedDay && selectedDay <= daysInMonth) {
      const dayToHighlight = document.querySelector(`.days li a[data-value="${selectedDay}"]`);
      if (dayToHighlight) {
        dayToHighlight.classList.add("selected");
        const date = new Date(year, month - 1, selectedDay);
        const dayOfWeek = dayNames[date.getDay()];
        dayInfoElement.textContent = `${dayOfWeek}, ${selectedDay}`;
      }
    }
  }

  function updateTaskList(date) {
    taskList.innerHTML = "";

    if (tasksByDate[date]) {
      tasksByDate[date].forEach((task) => {
        const li = document.createElement("li");
        li.textContent = task;
        taskList.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "Нет задач на сегодня";
      taskList.appendChild(li);
    }
  }

  function updateYear(newYear) {
    yearElement.textContent = newYear;
    const selectedMonth = parseInt(document.querySelector(".months a.selected").dataset.value);
    updateDays(selectedMonth, newYear);
  }

  months.forEach((month) => {
    month.addEventListener("click", () => {
      months.forEach((d) => d.classList.remove("selected"));
      month.classList.add("selected");

      const selectedMonth = parseInt(month.dataset.value);
      const year = parseInt(yearElement.textContent);

      monthNameElement.textContent = monthNames[selectedMonth - 1];
      updateDays(selectedMonth, year);
    });
  });

  prevYearButton.addEventListener("click", () => {
    const currentYear = parseInt(yearElement.textContent);
    updateYear(currentYear - 1);
  });

  nextYearButton.addEventListener("click", () => {
    const currentYear = parseInt(yearElement.textContent);
    updateYear(currentYear + 1);
  });

  updateDays(11, 2024);
  monthNameElement.textContent = monthNames[10];
  dayInfoElement.textContent = "Thursday, 14";
});
