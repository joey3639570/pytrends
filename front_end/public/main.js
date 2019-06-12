// Set the maximum number of input
const num_input = 5;
// Size of chart svg
var width = 800;
var height = 400;
// Initial Value before any keywords send
data={
    "name":"Go",
    "value":10
}

// Add input and button into input_list
var addInput = function(num){
    for(var i=0; i<num; i++){
        const name = "keyword " + i;
        const id = "keyword_"+i;
        var input_div = $('<div class="input-group input_box"><input type="text" class="form-control" id="'+id+'" placeholder="'+name+'" aria-label="'+name+'" aria-describedby="basic-addon2"><div class="input-group-append"><button id="'+id+"_btn"+'" class="btn btn-outline-secondary input_btn" type="button">Add</button></div></div>');
        input_div.appendTo('#input_list');
    }
}

var btn_click=function(e){
    var name = e.currentTarget.id;
    var id = "#"+name.substring(0, name.indexOf('_btn'));
    var text = $(id).val();

    $.ajax({
        method:"get",
        url:"./keyword?item="+text,
        success: function(data){
            console.log("Get data from keyword:");
            console.log(data);
        }
    })
    alert("New keyword added: " + text);
}

addInput(num_input);
$(".input_btn").on('click', btn_click);  // Must be called after inputs been added

pack = data => d3.pack()
    .size([width, height])
    .padding(3)
(d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value))

format = d3.format(",d")

color = d3.scaleLinear()
    .domain([0, 5])
    .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
    .interpolate(d3.interpolateHcl)

const root = pack(data);
let focus = root;
let view;
root.r = 400;

const svg = d3.select("body").select("svg")
    .attr("x", 0)
    .attr("y", 0)
    .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
    .style("display", "block")
    .style("margin", "0 -14px")
    .style("background", color(0))
    .style("cursor", "pointer")
    .on("click", () => zoom(root));

const node = svg.append("g")
    .selectAll("circle")
    .data(root.descendants().slice(1))
    .join("circle")
    .attr("fill", d => d.children ? color(d.depth) : "white")
    .attr("pointer-events", d => !d.children ? "none" : null)
    .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
    .on("mouseout", function() { d3.select(this).attr("stroke", null); })
    .on("click", d => focus !== d && (zoom(d), d3.event.stopPropagation()));

const label = svg.append("g")
    .style("font", "10px sans-serif")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .selectAll("text")
    .data(root.descendants())
    .join("text")
    .style("fill-opacity", d => d.parent === root ? 1 : 0)
    .style("display", d => d.parent === root ? "inline" : "none")
    .text(d => d.data.name);


function zoomTo(v) {
    const k = width / v[2];

    view = v;

    label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
    node.attr("r", d => d.r * k);
}

function zoom(d) {
    const focus0 = focus;

    focus = d;

    const transition = svg.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .tween("zoom", d => {
            const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
            return t => zoomTo(i(t));
        });

    label
        .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
        .transition(transition)
        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
}

svg.node();
zoomTo([root.x, root.y, root.r * 2]);
