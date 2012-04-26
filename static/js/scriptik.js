function hideMessage() {
    jQuery('#messages').hide();
}

function Content() {
    this.container = '';
    this.html = '';
    this.len = 0;
    ///
    this.Header = function(header) {
        this.len = header.length;
        this.html += '<tr>';
        ///
        for (var r in header) {
            this.html += '<th>' + header[r] + '</th>';
        }
        ///
        this.html += '</tr>';
    };
    ///
    this.Content = function(rows) {
        if (rows.length > 0) {
            for (var r in rows) {
                this.html += '<tr>';
                ///
                for (var d in rows[r]) {
                    this.html += '<td>' + rows[r][d] + '</td>';
                }
                ///
                this.html += '</tr>';
            }
        }
        else {
            this.html += '<tr><td align="center" colspan="' + this.len + '">Пусто</td></tr>';
        }
    };
    ///
    this.Start = function() {
        this.html = '<table>';
    };
    ///
    this.Stop = function() {
        this.html += '</table>';
        ///
        jQuery('#'+this.container).html(this.html);
    };
    ///
    this.init = function(container, data) {
        this.container = container;
        ///
        this.Start();
        this.Header(data.header);
        this.Content(data.rows);
        this.Stop();
    };
}

var oContent = new Content();

function getContent(container, t) {
    jQuery.ajax({
        type: 'get',
        url: '/content/?t='+t,
        data: '',
        dataType: 'json',
        success: function(data, status) {
            if (data.error == 0) {
                oContent.init(container, data);
            }
        },
        error: function(data, status, e) {
            alert(e);
        }
    });
}
