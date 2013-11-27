from IPython.display import HTML, display
VERSION = "0.1"

wordles = 0
def wordle(words,width=600,height=600,title=None) :
    global wordles
    html = """
<div id="wordle%(id)d"></div>
<script type="text/javascript">
var intID_wordle%(id)d = window.setInterval(
    function() {
        var wordle_id = '#wordle%(id)d';
        try {
            exports;
            if(exports.cloud && !d3.select(wordle_id).empty()) {
                wordle([%(words)s],
                       {target:wordle_id,
                        width:%(width)d,
                        height:%(height)d,
                        title:%(title)s
                       });
                window.clearInterval(intID_wordle%(id)d);
            }
        } catch(e) {
            console.log('d3-cloud not loaded yet:'+e);
        }
    },500);
</script>"""%{'id':wordles,
              'words':','.join('"%s"'%w for w in words),
              'width':width,
              'height':height,
              'title':'"'+str(title)+'"' if title else 'null'}
    wordles += 1
    display(HTML(html))

def setup_wordle() :
    html = """
        <script>
        var exports = {};
        </script>
        <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
        <script src="http://adamlabadorf.github.io/d3-cloud/d3.layout.cloud.js"></script>
        <script>
            //var fill = d3.scale.category20();
            var fill = function() { return "black"; };

            function wordle(words,opts) {

                var word_counts = {},
                    word_list = [],
                    opts = opts || {},
                    width, height,
                    title_bbox, title_transf,
                    font_size_scale = d3.scale.linear(),
                    count_min = 1e5, count_max = 0,
                    stopWords = ['in','on','of','or','to'],
                    i;

                opts.target = opts.target || "body";
                width = opts.width || 600;
                height = opts.height || 600;

                for(i=0; i < words.length; i++) {
                    if(stopWords.indexOf(words[i]) == -1) {
                        word_counts[words[i]] = (word_counts[words[i]] || 0) + 1;
                    }
                }

                for(i in word_counts) {
                    count_min = Math.min(word_counts[i],count_min);
                    count_max = Math.max(word_counts[i],count_max);
                    word_list.push({text:i,count:word_counts[i]});
                }
          
                font_size_scale
                    .domain([count_min,count_max])
                    .range([Math.max(10,14*width/600),56*height/600]);

                exports.cloud().size([width, height])
                    .words(word_list)
                    .padding(5)
                    .font("Impact")
                    .fontSize(function(d) { return font_size_scale(d.count); })
                    .on("end", draw)
                    .start();
            
                function draw(words) {
                    var svg = d3.select(opts.target).append("svg"),
                        title;
                    svg.append("rect")
                        .attr({"stroke":"black",
                               "fill":"none",
                               "width":width+"px",
                               "height":height+"px"
                            });

                    // do title in the background
                    if(opts.title) {
                        title = svg.append("text")
                            .attr({
                                    stroke:"none",
                                    fill:"#ddd",
                                    "font-size":128*height/600,
                                    dx:"0.2em",
                                    dy:"0.9em"
                                    })
                            .text(opts.title);
                        title_bbox = title.node().getBBox();
                        console.log(title_bbox);
                        if(title_bbox.width > width) {
                            title_transf = "scale("+width/title_bbox.width+")";
                        }
                        title.attr("transform",title_transf);
                    }
                    
                    svg
                        .attr("width", width)
                        .attr("height", height)
                        .append("g")
                        .attr("transform", "translate("+~~(width/2)+","+~~(height/2)+")")
                        .selectAll("text")
                        .data(words)
                        .enter().append("text")
                        .style("font-size", function(d) { return d.size + "px"; })
                        .style("font-family", "Impact")
                        .style("fill", function(d, i) { return fill(i); })
                        .attr("text-anchor", "middle")
                        .attr("transform", function(d) {
                            return "translate(" + [d.x, d.y] + ")rotate("+d.rotate+")";
                         })
                        .text(function(d) { return d.text; })
                        .on("mouseover",function(d) { console.log(d); });
                }
            }
        </script>
        ipynb wordle setup, version %s<br/>
        call like:<br/> <code>wordle(['list','of','words'],width=600,height=300,title="The Good Stuff")</code>"""%VERSION
    display(HTML(html))

setup_wordle()
