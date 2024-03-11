const tableDiv = document.getElementById('table');

const updateUrl = (prev, query) => {
  return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
};

const editableCellAttributes = (data, row, col) => {
    if (row) {
      return {contentEditable: 'true', 'data-element-id': row.cells[0].data};
    }
    else {
      return {};
    }
};

new gridjs.Grid({
  columns: [
    { id: 'id', 'hidden': true },
    { id: 'title', name: 'Title', 'attributes': editableCellAttributes },
    { id: 'grant_title', name: 'Grant Title' },
    { id: 'lead_pi', name: 'Lead PI', 'attributes': editableCellAttributes },
    { id: 'starting_trl', name: 'Starting TRL', sort: false },
    { id: 'anticipated_ending_trl', name: 'Anticipated Ending TRL', sort: false },
    { id: 'description', name: 'Description', sort: false, 'attributes': editableCellAttributes },
    { id: 'author', name: 'Author' },
  ],
  server: {
    url: '/api/data',
    then: results => results.data,
    total: results => results.total,
  },
  search: {
    enabled: true,
    server: {
      url: (prev, search) => {
        return updateUrl(prev, {search});
      },
    },
  },
  sort: {
    enabled: true,
    multiColumn: true,
    server: {
      url: (prev, columns) => {
        const columnIds = ['id', 'lead_pi'];
        const sort = columns.map(col => (col.direction === 1 ? '+' : '-') + columnIds[col.index]);
        return updateUrl(prev, {sort});
      },
    },
  },
  pagination: {
    enabled: true,
    server: {
      url: (prev, page, limit) => {
        return updateUrl(prev, {start: page * limit, length: limit});
      },
    },
  },
}).render(tableDiv);

let savedValue;

tableDiv.addEventListener('focusin', ev => {
  if (ev.target.tagName === 'TD') {
    savedValue = ev.target.textContent;
  }
});

tableDiv.addEventListener('focusout', ev => {
  if (ev.target.tagName === 'TD') {
    if (savedValue !== ev.target.textContent) {
      fetch('/api/data', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          id: ev.target.dataset.elementId,
          [ev.target.dataset.columnId]: ev.target.textContent
        }),
      });
    }
    savedValue = undefined;
  }
});

tableDiv.addEventListener('keydown', ev => {
  if (ev.target.tagName === 'TD') {
    if (ev.key === 'Escape') {
      ev.target.textContent = savedValue;
      ev.target.blur();
    }
    else if (ev.key === 'Enter') {
      ev.preventDefault();
      ev.target.blur();
    }
  }
});