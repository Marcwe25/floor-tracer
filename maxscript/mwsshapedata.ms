struct shapeDataStructure (

    public kposition = #(),
    public kmatId = #(),
    public kwidth = #(),
    public kisClosed = #(),
    public reverseIndx = #(),
    public segmentLenght = #(),
    public indx = #(),

    private bdb = undefined,

    public shapeArray = undefined,

    public fn getIndex index = (
        indx[index[1]][index[2]][index[3]]
    ),

    public fn getPosition index = (
        kposition[index[1]][index[2]][index[3]]
    ),

    public fn getReverseIndx index = (
        reverseIndx[index[1]][index[2]][index[3]]
    ),

    public fn getMatId index = (
        kmatId[index[1]][index[2]][index[3]]
    ),

    public fn getClosed index = (
        kisClosed[index[1]][index[2]]
    ),

    public fn nextKnot index cycling= (
        lastKnot = kposition[index[1]][index[2]].count
        next = #(index[1],index[2],index[3]+1)
        if (next[3]==lastKnot+1) then (
            if cycling then (
                next[3]=1
            ) else return undefined)
        if (next[3]<1 or next[3]>lastKnot) then return undefined
        getIndex next
    ),

    public fn prevKnot index = (
        lastKnot = kposition[index[1]][index[2]].count
        prev = #(index[1],index[2],index[3]-1)
        if (prev[3]==0) then (
            if cycling then (
                prev[3]==lastKnot
            ) else return undefined)
        if (prev[3]<1 or prev[3]>lastKnot) then return undefined
        getIndex prev
    ),

    public fn getSegment index = (
        lastKnot = kposition[index[1]][index[2]].count
        nextStart = #(index[1],index[2],index[3])
        nextEnd = #(index[1],index[2],index[3]+1)

        if (nextStart[3]==lastKnot) then (
            if kisClosed[index[1]][index[2]]
            then (nextEnd[3]=1)
            else (
                return undefined
            )
        )

        if (nextStart[3]<1 or nextEnd[3]>lastKnot) then return undefined
        #(getIndex nextStart,getIndex nextEnd)
    ),

    public fn nextSegment index cycling= (
        lastKnot = kposition[index[1]][index[2]].count
        nextStart = #(index[1],index[2],index[3]+1)
        nextEnd = #(index[1],index[2],index[3]+2)

        if (nextStart[3]==lastKnot) then (
            if kisClosed[index[1]][index[2]]
            then (nextEnd[3]=1)
            else (
                if cycling 
                then (
                    nextStart[3]=1
                    nextEnd[3]=2) 
                else return undefined
            )
        )

        if (nextStart[3]==lastKnot+1) 
        then (
                if cycling 
                then (
                    nextStart[3]=1
                    nextEnd[3]=2) 
                else return undefined
            )
        if (nextStart[3]<1 or nextEnd[3]>lastKnot) then return undefined
        #(getIndex nextStart,getIndex nextEnd)
    ),

    public fn prevSegment index cycling = (
        lastKnot = kposition[index[1]][index[2]].count
        prevStart = #(index[1],index[2],index[3]-1)
        prevEnd = #(index[1],index[2],index[3])

        if (prevStart[3]==0) then (
            if cycling 
            then (
                if kisClosed[index[1]][index[2]]
                then (
                    prevStart[3]=lastKnot
                    prevEnd[3]=1)
                else (
                    prevStart[3] = lastKnot-1
                    prevEnd[3] = lastKnot)
                )
            else return undefined
        )
        if (prevStart[3]<1 or prevEnd[3]>lastKnot) then return undefined
        #(getIndex prevStart,getIndex prevEnd)
    
    ),

    fn comparePointX i1 i2 = (
        p1 = getPosition i1
        p2 = getPosition i2
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    fn comparePointY i1 i2 = (
        p1 = getPosition i1
        p2 = getPosition i2
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    fn compareSegmentX s1 s2 = (
        p1 = getPosition s1[1]
        p2 = getPosition s2[1]
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    fn compareSegmentY s1 s2 = (
        p1 = getPosition s1[1]
        p2 = getPosition s2[1]
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    fn compareEndSegmentX s1 s2 = (
        p1 = getPosition s2[1]
        p2 = getPosition s2[1]
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    fn compareEndSegmentY s1 s2 = (
        p1 = getPosition s2[1]
        p2 = getPosition s2[1]
        case of (
            (close_enough p1.x p2.x 3) : 0
            (p1.x>p2.x) : 1
            (p1.x<p2.x) : -1
            default: 0
        )
    ),

    public fn evaluateSegmentLength = (
        for ishape = 1 to kposition.count   do (
            append segmentLength #()
            for ispline = 1 to kposition[ishape].count   do (
                append segmentLength[ishape] #()
                for iknot = 1 to (kposition[ishape][ispline].count-1)   do (
                    d = distance kposition[ishape][ispline][iknot+1] kposition[ishape][ispline][iknot]
                    append segmentLength[ishape][ispline] d
                )
            )        )
    ),

	public fn setbdb = (
        bdb = #(#(),#())
        for ishape in kposition  do (
            for ispline in ishape do (
                for iknot in ispline do (
                    append bdb[1] iknot.x
                    append bdb[2] iknot.y
                )
            )
        )
    ),
	
    public fn getbdb = (
        setbdb()
        bdb
    ),


    public fn appendEmptyShape = (
        append kposition  #()
        append kmatId  #()
        append kwidth  #()
        append kisClosed  #()
        append reverseIndx #()
        append indx #()
        --  append segmentAngle #()
    ),
    
    public fn appendEmptySpline = (
        last = kposition.count
        append kposition[last] #()
        append kmatId[last] #()
        append kwidth[last] #()
        append kisClosed[last] #()
        append reverseIndx[last] #()
        append indx[last] #()
    --    append segmentAngle[last] #()
    ),

    public fn initializeSizeFromShape = (
        for ishape = 1 to shapeArray.count do (
            appendEmptyShape()
            for kspline = 1 to (numSplines shapeArray[ishape]) do (
                appendEmptySpline()
            )
        )
    ),

    public fn buildDataFromShape = (

        for ishape = 1 to shapeArray.count do (
            for ispline = 1 to (numSplines shapeArray[ishape]) do (

                kisClosed[ishape][ispline] = (isClosed shapeArray[ishape] ispline)

                numOfKnots = numKnots shapeArray[ishape] ispline
                for iknot = 1 to (numOfKnots - 1) do (
                    kposition[ishape][ispline][iknot] =  getKnotPoint shapeArray[ishape] ispline iknot
                    kmatId[ishape][ispline][iknot] = getMaterialID shapeArray[ishape] ispline iknot
                --    segmentAngle[ishape][ispline][iknot] = getPiAngleOfVector ((getKnotPoint shapeArray[ishape] ispline iknot+1) - kposition[ishape][ispline][iknot]) [1,0,0]
                )

                kposition[ishape][ispline][numOfKnots]  = getKnotPoint shapeArray[ishape] ispline numOfKnots

                if (kisClosed[ishape][ispline]) then (
                    kmatId[ishape][ispline][numOfKnots] = getMaterialID shapeArray[ishape] ispline numOfKnots
                --    segmentAngle[ishape][ispline][iknot] = getPiAngleOfVector ((kposition[ishape][ispline][1] - kposition[ishape][ispline][iknot]) [1,0,0]
                )
            )
        )
    ),

    fn printPosition = (
        for ishape = 1 to kposition.count  do (
            for ispline = 1 to kposition[ishape].count  do (
                for iknot = 1 to kposition[ishape][ispline].count  do (
                    ----print(ishape as string + " " +ispline  as string +" " + iknot as string + " " + kposition[ishape][ispline][iknot] as string)
                )
            )
        )
    ),
	
	on create do (
        if shapeArray != undefined then (
            initializeSizeFromShape()
            buildDataFromShape()
        )
    )
)
 