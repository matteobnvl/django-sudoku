
const elements = document.querySelectorAll('td')
const chiffres = document.querySelectorAll('.choose-number div')
let selected = null
let arrayCase = {}
const url = 'http://127.0.0.1:8000/'
const id_sudoku = document.querySelectorAll('span#id_sudoku')

elements.forEach(function(item) {
    item.addEventListener('click', function(event) {
        if ($(item).attr('data-finish') != 1) {
            elements.forEach(function(item) {
                item.classList.remove('selected')
            })
            item.classList.add('selected')
            selected = item
            }
        })
})

chiffres.forEach(function(item) {
    item.addEventListener('click', function(event) {
        if (selected !== null && $(selected).attr('data-td') === undefined) {
            attrCase = $(selected).attr('data-row')
            if ($(item).attr('data-del') == "1") {
                selected.textContent = ''
                selected.className = ''
                $.ajax({
                    url: `${url}/delete`,
                    type: 'POST',
                    data: {attrCase: attrCase, id: id_sudoku}
                })
            } else if ($(item).attr('data-check') != "1" && $(item).attr('data-verif') != "1") {
                selected.textContent = item.textContent
                selected.className = ''
                arrayCase = {key: attrCase , value: item.textContent}
                $.ajax({
                    url: `${url}/insert`,
                    type: 'POST',
                    data: {arrayCase: arrayCase, id: id_sudoku}
                })
            }
        }
    })
})

$('div[data-check]').click(function () {
    $.ajax({
        url: `${url}/verif`,
        type: 'POST',
        data: {id: id_sudoku},
        success: function (response) {
            if (response != 'false') {
                response = JSON.parse(response)
                vie = parseInt($('#vie').html())
                vie--
                $('#vie').html(vie.toString())
                elements.forEach(function (item) {
                    response.forEach(function (event) {
                        if ($(item).attr('data-row') == event.key) {
                            $(item).addClass((event.value)? 'true' : 'false')
                        }
                    })
                })
            } else {
                vie = parseInt($('#vie').html())
                vie--
                $('#vie').html(vie.toString())
                $('#toggleVie').addClass('active')
                elements.forEach(function (item) {
                        item.setAttribute('data-finish', '1')
                })
            }
        }
    })
})

$('div[data-verif]').click(function () {
    var finish = true
    elements.forEach(function (item) {
        if (item.textContent == 0) {
            finish = false
        }
    })
    if (finish) {
        $.ajax({
            url: `${url}/finish`,
            type: 'POST',
            data: {id: id_sudoku},
            success: function (response) {
                response = JSON.parse(response)
                if (response.key == true) {
                    elements.forEach(function (item) {
                        item.setAttribute('data-finish', '1')
                    })
                    $('#toggleWin').addClass('active')
                    $('#reussi').html('Bravo tu as réussi ce sudoku !!')
                    $('#score').html(response.score)
                } else {
                    elements.forEach(function (item) {
                        response.forEach(function (event) {
                            if ($(item).attr('data-row') == event.key) {
                                $(item).addClass((event.value)? 'true' : 'false')
                            }
                        })
                    })
                }
            }
        })
    }
})
